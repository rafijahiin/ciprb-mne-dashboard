import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.apps import apps
from baseline.models import BaselineAssessment
from baseline.utils import KOBO_MAPPINGS


class KoboIngestView(APIView):
    def post(self, request, *args, **kwargs):
        # 1. Secure the endpoint by checking the HTTP_X_KOBO_WEBHOOK_SECRET
        secret = request.META.get('HTTP_X_KOBO_WEBHOOK_SECRET')
        # Using 'test_secret' as a fallback for local testing
        expected_secret = os.environ.get('KOBO_WEBHOOK_SECRET')
        if not expected_secret:
            from django.core.exceptions import ImproperlyConfigured
            raise ImproperlyConfigured("KOBO_WEBHOOK_SECRET environment variable is required.")

        if secret != expected_secret:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        payload = request.data
        form_type = payload.get('form_type')
        kobo_submission_id = payload.get('kobo_submission_id')

        if not form_type or not kobo_submission_id:
            return Response({"error": "Missing form_type or kobo_submission_id"}, status=status.HTTP_400_BAD_REQUEST)

        if form_type == 'fistula_campaign':
            model = apps.get_model('tracker', 'FistulaCase')
            # Check for duplicates
            if model.objects.filter(kobo_submission_id=kobo_submission_id).exists():
                return Response({"message": "Duplicate submission ignored"}, status=status.HTTP_200_OK)

            # Map fields using utils mapping
            mapping = KOBO_MAPPINGS.get(
                'fistula_campaign', {}).get('fields', {})
            data = {}
            for kobo_field, model_field in mapping.items():
                if kobo_field in payload:
                    data[model_field] = payload[kobo_field]

            data['kobo_submission_id'] = kobo_submission_id

            try:
                model.objects.create(**data)
                return Response({"message": "FistulaCase created successfully"}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        elif form_type == 'mpdsr_report':
            model = apps.get_model('mpdsr', 'MPDSREvent')
            # Check for duplicates
            if model.objects.filter(kobo_submission_id=kobo_submission_id).exists():
                return Response({"message": "Duplicate submission ignored"}, status=status.HTTP_200_OK)

            # Map fields using utils mapping
            mapping = KOBO_MAPPINGS.get('mpdsr_report', {}).get('fields', {})
            data = {}
            for kobo_field, model_field in mapping.items():
                if kobo_field in payload:
                    data[model_field] = payload[kobo_field]

            data['kobo_submission_id'] = kobo_submission_id

            try:
                model.objects.create(**data)
                return Response({"message": "MPDSREvent created successfully"}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        elif form_type == 'baseline_assessment':
            if BaselineAssessment.objects.filter(kobo_submission_id=kobo_submission_id).exists():
                return Response({"message": "Duplicate submission ignored"}, status=status.HTTP_200_OK)

            try:
                partner = payload.get('partner', 'Unknown')
                BaselineAssessment.objects.create(
                    partner=partner,
                    payload=payload,
                    kobo_submission_id=kobo_submission_id
                )
                return Response({"message": "BaselineAssessment created successfully"}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": f"Unknown form_type: {form_type}"}, status=status.HTTP_400_BAD_REQUEST)
