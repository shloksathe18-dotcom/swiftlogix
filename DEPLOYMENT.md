# Deploying SwiftLogix to Render

This guide explains how to deploy the SwiftLogix application to Render for production hosting.

## Prerequisites

1. A Render account (https://render.com)
2. A GitHub account with the SwiftLogix repository

## Deployment Steps

### 1. Fork the Repository

First, fork the SwiftLogix repository to your GitHub account if you haven't already.

### 2. Create a New Web Service on Render

1. Go to your Render dashboard
2. Click "New" and select "Web Service"
3. Connect your GitHub account and select your SwiftLogix repository
4. Configure the service:
   - Name: `swiftlogix` (or any name you prefer)
   - Region: Choose the region closest to your users
   - Branch: `main` (or your default branch)
   - Root Directory: Leave empty
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn --bind 0.0.0.0:$PORT backend.app:app`

### 3. Configure Environment Variables

In the Render dashboard, go to your service settings and add these environment variables:

```
FLASK_APP=backend.app:create_app
FLASK_ENV=production
SECRET_KEY=your-super-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
DATABASE_URL=sqlite:///swiftlogix.db
SECURE_COOKIES=true
```

Important: Replace the secret keys with strong, random values for production.

### 4. Deploy

Click "Create Web Service" to start the deployment. Render will:

1. Clone your repository
2. Install dependencies using the requirements.txt file
3. Build and deploy your application

### 5. Initialize the Database

After the first deployment, you'll need to initialize the database:

1. Go to your service dashboard on Render
2. Click "Shell" to open a terminal
3. Run these commands:
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

### 6. Access Your Application

Once deployed, your application will be available at `https://your-service-name.onrender.com`

## Custom Domain (Optional)

To use a custom domain:

1. In your Render service dashboard, go to "Settings"
2. Scroll to "Custom Domains"
3. Add your domain and follow the instructions to configure DNS

## Environment Variables

Here are the key environment variables you should configure:

| Variable | Description | Example Value |
|----------|-------------|---------------|
| `FLASK_APP` | Flask application entry point | `backend.app:create_app` |
| `FLASK_ENV` | Environment mode | `production` |
| `SECRET_KEY` | Flask secret key | `your-secret-key-here` |
| `JWT_SECRET_KEY` | JWT secret key | `your-jwt-secret-here` |
| `DATABASE_URL` | Database connection string | `sqlite:///swiftlogix.db` |
| `SECURE_COOKIES` | Enable secure cookies | `true` |

## Scaling Considerations

For production use, consider:

1. Using a managed database service (PostgreSQL, MySQL) instead of SQLite
2. Adding a CDN for static assets
3. Configuring auto-scaling based on traffic
4. Setting up monitoring and logging

## Troubleshooting

### Database Issues

If you encounter database errors:

1. Ensure you've run the database initialization commands
2. Check that the `DATABASE_URL` environment variable is correctly set
3. For persistent data, consider using Render's managed PostgreSQL service

### Build Failures

If the build fails:

1. Check that all dependencies are listed in `requirements.txt`
2. Ensure the build command is correct
3. Check the build logs for specific error messages

### Application Errors

If the application fails to start:

1. Check the application logs in the Render dashboard
2. Verify all environment variables are correctly set
3. Ensure the start command is correct

## Updating Your Application

To update your deployed application:

1. Push changes to your GitHub repository
2. Render will automatically detect the changes and start a new deployment
3. Monitor the deployment progress in the dashboard

## Support

For issues with deployment:

1. Check the Render documentation: https://render.com/docs
2. Review the application logs in your Render dashboard
3. Ensure your repository structure matches the expected format
