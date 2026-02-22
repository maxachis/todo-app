from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from tasks.services.outlook_auth import (
    acquire_token_by_device_code,
    acquire_token_silent,
    initiate_device_code_flow,
)


class Command(BaseCommand):
    help = "Authenticate with Microsoft Graph API using the Device Code flow"

    def handle(self, *args, **options):
        if not settings.OUTLOOK_CLIENT_ID:
            raise CommandError(
                "OUTLOOK_CLIENT_ID is not configured. "
                "Set it in your environment or Django settings."
            )

        # Check if already authenticated
        token = acquire_token_silent()
        if token:
            self.stdout.write(self.style.SUCCESS("Already authenticated with valid tokens."))
            self.stdout.write("Run with --force to re-authenticate.")
            return

        self.stdout.write("Starting Microsoft Graph API authentication...")
        self.stdout.write("")

        app, flow, cache = initiate_device_code_flow()

        self.stdout.write(flow["message"])
        self.stdout.write("")
        self.stdout.write("Waiting for authorization...")

        result = acquire_token_by_device_code(app, flow, cache)

        if "access_token" in result:
            self.stdout.write(self.style.SUCCESS("Authentication successful!"))
            self.stdout.write(
                f"Token cache saved to: {settings.OUTLOOK_TOKEN_CACHE_FILE}"
            )
        else:
            error = result.get("error_description", result.get("error", "Unknown error"))
            raise CommandError(f"Authentication failed: {error}")
