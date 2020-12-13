function httpReq(options)
{
    options.onSuccess = options.onSuccess || function(e) {};
    options.onError = options.onError || function(e) {};
    options.method = options.method || 'GET';
    options.url = options.url || null;
    options.args = options.args || null;
    
    req = new XMLHttpRequest();
    req.open(options.method,options.url,false);
    req.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    req.onreadystatechange = function (e) {
        if (req.readyState === 4) {
            if(req.status == 200)
            {
                options.onSuccess(req.responseText);
            }
            else 
            {
                options.onError(req.status);
            }
        }
        }
    req.send(options.args);
}