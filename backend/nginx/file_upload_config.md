# Nginx Configuration for Large File Uploads

To allow larger file uploads in Nginx, you need to modify your Nginx configuration file. Here's how to do it:

## 1. Locate your Nginx configuration file

The main Nginx configuration file is typically located at:
```
/etc/nginx/nginx.conf
```

And your site-specific configuration might be at:
```
/etc/nginx/sites-available/snownavi.ski
```

## 2. Add or modify the following directives

Add these directives to the `http` section of your nginx.conf or to your site-specific configuration:

```nginx
http {
    # Existing configuration...
    
    # Increase the client body size to allow larger uploads (16MB)
    client_max_body_size 16M;
    
    # Increase buffer size for file uploads
    client_body_buffer_size 128k;
    
    # Increase timeouts for larger uploads
    client_body_timeout 60s;
    client_header_timeout 60s;
    keepalive_timeout 60s;
    send_timeout 60s;
    
    # Rest of your configuration...
}
```

If you're adding it to your site-specific configuration, you can add it inside the `server` block:

```nginx
server {
    # Existing configuration...
    
    # Increase the client body size to allow larger uploads (16MB)
    client_max_body_size 16M;
    
    # Rest of your configuration...
}
```

## 3. Test and reload Nginx

After making changes, test the configuration:

```bash
sudo nginx -t
```

If the test is successful, reload Nginx:

```bash
sudo systemctl reload nginx
```

## 4. Verify the changes

After reloading Nginx, try uploading a larger file to verify that the changes have taken effect.

## Note

The `client_max_body_size` directive sets the maximum allowed size of the client request body. This determines the maximum size of files that can be uploaded through Nginx. Make sure this value matches or exceeds the `MAX_CONTENT_LENGTH` value set in your Flask application (16MB in this case).
