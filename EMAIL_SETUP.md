# Email Setup Instructions

To enable email functionality in the Logistics App, you need to configure Gmail with an App Password.

## Steps to Create a Gmail App Password

1. **Sign in to your Google Account**
   - Go to https://myaccount.google.com/
   - Sign in with the credentials for swiftlogixindia@gmail.com

2. **Enable 2-Step Verification**
   - In the left navigation panel, select "Security"
   - Under "Signing in to Google," confirm that 2-Step Verification is turned on
   - If not, click "2-Step Verification" and follow the steps to set it up

3. **Generate an App Password**
   - In the "Signing in to Google" section, click "App passwords"
   - If you don't see this option, 2-Step Verification is not enabled
   - Under "Select app," choose "Mail"
   - Under "Select device," choose "Other" and give it a name like "Logistics App"
   - Click "Generate"
   - Copy the 16-character password that appears

4. **Configure the Application**
   - Set the `GMAIL_APP_PASSWORD` environment variable with the generated password:
     ```bash
     export GMAIL_APP_PASSWORD="your-16-character-app-password"
     ```
   - On Windows:
     ```cmd
     set GMAIL_APP_PASSWORD=your-16-character-app-password
     ```

5. **Restart the Application**
   - Stop the current application (Ctrl+C)
   - Start the application again to use the new configuration

## Security Notes

- App passwords are separate from your regular Google Account password
- App passwords can only be used with accounts that have 2-Step Verification turned on
- You should limit access to the App password and treat it like any other password
- If you suspect the App password has been compromised, revoke it and generate a new one

## Testing Email Functionality

After configuring the App Password:

1. Register a new user through the API
2. Check swiftlogixindia@gmail.com for notification emails
3. For admin users, use the approval link in the email to approve the account
4. Check for confirmation emails after approval

## Troubleshooting

If emails are not being sent:

1. Verify the App Password is correct
2. Check that 2-Step Verification is enabled
3. Ensure the Gmail account is not blocked for security reasons
4. Check the application logs for any error messages
5. Verify that the Gmail account allows sending emails through SMTP