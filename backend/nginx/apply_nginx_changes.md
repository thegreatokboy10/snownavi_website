# Applying Nginx Configuration Changes

Follow these steps to apply the updated Nginx configuration with file upload size limits:

## 1. Copy the updated configuration file to the server

```bash
# Copy the updated configuration file to the Nginx sites-available directory
sudo cp backend/nginx/snownavi.ski /etc/nginx/sites-available/
```

## 2. Test the Nginx configuration

Before reloading Nginx, it's important to test the configuration to ensure there are no syntax errors:

```bash
sudo nginx -t
```

If the test is successful, you should see output similar to:
```
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
```

## 3. Reload Nginx to apply the changes

If the test was successful, reload Nginx to apply the changes:

```bash
sudo systemctl reload nginx
```

## 4. Verify the changes

After reloading Nginx, try uploading a file to verify that the changes have taken effect. You should now be able to upload files up to 16MB in size.

## 5. Check Nginx logs if issues persist

If you still encounter issues with file uploads, check the Nginx error logs:

```bash
sudo tail -f /var/log/nginx/error.log
```

## Summary of Changes

The following changes were made to the Nginx configuration:

1. Added file upload settings to the server block:
   - `client_max_body_size 16M` - Allows uploads up to 16MB
   - `client_body_buffer_size 128k` - Increases buffer size for file uploads
   - `client_body_timeout 60s` - Increases timeout for larger uploads
   - `client_header_timeout 60s` - Increases header timeout
   - `keepalive_timeout 60s` - Increases keepalive timeout
   - `send_timeout 60s` - Increases send timeout

2. Updated the location block for admin and API endpoints:
   - Added `/uploads/` to the location pattern
   - Added `proxy_send_timeout 300s` - Increases send timeout
   - Added `proxy_request_buffering off` - Disables request buffering for large file uploads
   - Added `proxy_buffering off` - Disables response buffering

These changes ensure that Nginx can handle larger file uploads and properly proxy them to the Flask server.
