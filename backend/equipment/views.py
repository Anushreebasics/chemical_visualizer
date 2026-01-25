from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token as AuthToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Avg, Count, Q
from django.http import HttpResponse
import pandas as pd
import io
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib import colors

from equipment.models import Equipment, DataUpload, UserProfile
from equipment.serializers import (
    EquipmentSerializer, DataUploadSerializer, DataSummarySerializer, 
    UploadCSVSerializer, UserSerializer
)


class UserRegisterView(generics.CreateAPIView):
    """API view for user registration"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        first_name = request.data.get('first_name', '')
        last_name = request.data.get('last_name', '')
        
        if not username or not password:
            return Response({'error': 'Username and password are required'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        # Token for the new user (profile is auto-created via signal)
        token, _ = AuthToken.objects.get_or_create(user=user)
        
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key,
            'message': 'User registered successfully'
        }, status=status.HTTP_201_CREATED)


class UserLoginView(generics.GenericAPIView):
    """API view for user login"""
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(username=username, password=password)
        
        if user is None:
            return Response({'error': 'Invalid credentials'}, 
                          status=status.HTTP_401_UNAUTHORIZED)
        
        token, _ = AuthToken.objects.get_or_create(user=user)
        
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key,
            'message': 'Login successful'
        }, status=status.HTTP_200_OK)


class UserLogoutView(generics.GenericAPIView):
    """API view for user logout"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        request.user.auth_token.delete()
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)


class EquipmentViewSet(viewsets.ModelViewSet):
    """ViewSet for Equipment model"""
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return equipment for the current user only"""
        user = self.request.user
        return Equipment.objects.filter(upload__user=user)


class UploadCSVView(generics.CreateAPIView):
    """API view for CSV file upload and processing"""
    serializer_class = UploadCSVSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        csv_file = serializer.validated_data['file']
        
        try:
            # Read CSV file
            df = pd.read_csv(io.StringIO(csv_file.read().decode('utf-8')))
            
            # Validate required columns
            required_columns = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
            if not all(col in df.columns for col in required_columns):
                return Response(
                    {'error': f'CSV must contain columns: {", ".join(required_columns)}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Clean column names
            df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]
            
            # Create DataUpload record
            upload = DataUpload.objects.create(
                user=request.user,
                filename=csv_file.name,
                total_records=len(df)
            )
            
            # Process and save equipment data
            for _, row in df.iterrows():
                try:
                    equipment_type = str(row['type']).lower().strip()
                    # Map common type names
                    type_mapping = {
                        'pump': 'pump', 'compressor': 'compressor', 'reactor': 'reactor',
                        'heat exchanger': 'heat_exchanger', 'separator': 'separator',
                        'mixer': 'mixer', 'boiler': 'boiler', 'filter': 'filter'
                    }
                    equipment_type = type_mapping.get(equipment_type, 'other')
                    
                    Equipment.objects.create(
                        upload=upload,
                        equipment_name=str(row['equipment_name']).strip(),
                        equipment_type=equipment_type,
                        flowrate=float(row['flowrate']),
                        pressure=float(row['pressure']),
                        temperature=float(row['temperature'])
                    )
                except (ValueError, KeyError) as e:
                    continue
            
            # Calculate summary statistics
            equipment_items = upload.equipment_items.all()
            if equipment_items.exists():
                upload.avg_flowrate = equipment_items.aggregate(Avg('flowrate'))['flowrate__avg'] or 0
                upload.avg_pressure = equipment_items.aggregate(Avg('pressure'))['pressure__avg'] or 0
                upload.avg_temperature = equipment_items.aggregate(Avg('temperature'))['temperature__avg'] or 0
                upload.save()
            
            # Keep only last 5 uploads
            old_uploads = DataUpload.objects.filter(user=request.user).order_by('-uploaded_at')[5:]
            for old_upload in old_uploads:
                old_upload.equipment_items.all().delete()
                old_upload.delete()
            
            return Response(
                DataUploadSerializer(upload).data,
                status=status.HTTP_201_CREATED
            )
        
        except Exception as e:
            return Response(
                {'error': f'Error processing CSV: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )


class DataSummaryView(generics.GenericAPIView):
    """API view for getting data summary"""
    permission_classes = [IsAuthenticated]
    serializer_class = DataSummarySerializer
    
    def get(self, request):
        user = request.user
        user_equipment = Equipment.objects.filter(upload__user=user)
        
        if not user_equipment.exists():
            return Response({
                'total_count': 0,
                'avg_flowrate': 0,
                'avg_pressure': 0,
                'avg_temperature': 0,
                'equipment_type_distribution': {},
                'recent_uploads': []
            })
        
        # Calculate statistics
        total_count = user_equipment.count()
        avg_flowrate = user_equipment.aggregate(Avg('flowrate'))['flowrate__avg'] or 0
        avg_pressure = user_equipment.aggregate(Avg('pressure'))['pressure__avg'] or 0
        avg_temperature = user_equipment.aggregate(Avg('temperature'))['temperature__avg'] or 0
        
        # Equipment type distribution
        type_dist = user_equipment.values('equipment_type').annotate(count=Count('id'))
        equipment_type_distribution = {item['equipment_type']: item['count'] for item in type_dist}
        
        # Recent uploads
        recent_uploads = DataUpload.objects.filter(user=user).order_by('-uploaded_at')[:5]
        
        data = {
            'total_count': total_count,
            'avg_flowrate': round(avg_flowrate, 2),
            'avg_pressure': round(avg_pressure, 2),
            'avg_temperature': round(avg_temperature, 2),
            'equipment_type_distribution': equipment_type_distribution,
            'recent_uploads': DataUploadSerializer(recent_uploads, many=True).data
        }
        
        return Response(data)


class HistoryListView(generics.ListAPIView):
    """API view for getting upload history"""
    serializer_class = DataUploadSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return DataUpload.objects.filter(user=self.request.user).order_by('-uploaded_at')[:5]


class GeneratePDFView(generics.GenericAPIView):
    """API view for generating PDF report"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, upload_id=None):
        user = request.user
        
        if upload_id:
            upload = get_object_or_404(DataUpload, id=upload_id, user=user)
        else:
            upload = DataUpload.objects.filter(user=user).latest('uploaded_at')
        
        # Create PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="report_{upload.id}_{datetime.now().strftime("%Y%m%d")}.pdf"'
        
        # Create PDF document
        doc = SimpleDocTemplate(response, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1f4788'),
            spaceAfter=30,
            alignment=1
        )
        elements.append(Paragraph('Chemical Equipment Analysis Report', title_style))
        elements.append(Spacer(1, 0.3*inch))
        
        # Header info
        header_data = [
            ['Report Date:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
            ['Upload File:', upload.filename],
            ['Total Records:', str(upload.total_records)],
        ]
        header_table = Table(header_data, colWidths=[2*inch, 4*inch])
        header_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f4f8')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ]))
        elements.append(header_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Summary statistics
        elements.append(Paragraph('Summary Statistics', styles['Heading2']))
        summary_data = [
            ['Metric', 'Value'],
            ['Average Flowrate', f"{upload.avg_flowrate:.2f}"],
            ['Average Pressure', f"{upload.avg_pressure:.2f}"],
            ['Average Temperature', f"{upload.avg_temperature:.2f}"],
        ]
        summary_table = Table(summary_data, colWidths=[3*inch, 3*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(summary_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Equipment list
        elements.append(Paragraph('Equipment Details', styles['Heading2']))
        equipment_items = upload.equipment_items.all()
        eq_data = [['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']]
        for eq in equipment_items[:20]:  # Limit to 20 items per page
            eq_data.append([
                eq.equipment_name,
                eq.equipment_type,
                f"{eq.flowrate:.2f}",
                f"{eq.pressure:.2f}",
                f"{eq.temperature:.2f}"
            ])
        
        eq_table = Table(eq_data, colWidths=[1.5*inch, 1.2*inch, 1.1*inch, 1.1*inch, 1.1*inch])
        eq_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')]),
        ]))
        elements.append(eq_table)
        
        # Build PDF
        doc.build(elements)
        return response
    
    def post(self, request):
        """Handle POST request with optional upload_id"""
        upload_id = request.data.get('upload_id')
        return self.get(request, upload_id)
