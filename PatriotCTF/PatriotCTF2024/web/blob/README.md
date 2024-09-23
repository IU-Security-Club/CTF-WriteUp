# BLOB Patriot CTF 2024
@phulelouch
### Problem:
```
require("express")()
  .set("view engine", "ejs")
  .use((req, res) => res.render("index", { blob: "blob", ...req.query }))
  .listen(3000);

```

### Way of thinking :
This problem is a classic example of a web vulnerability, specifically a template injection vulnerability. 
The code include ejs, (when saw it at this point you should look up ejs vulnerabilities) a templating engine, which allows us to inject arbitrary code into the template. 
The code is vulnerable to template injection because it uses the `res.render()` method to render 
###  Solution:

https://github.com/mde/ejs/issues/735

![alt text](<Sept 22 Screenshot from Discord.png>)


![alt text](<Screenshot 2024-09-22 at 4.37.17 PM.png>)