# yowsup-queue
This Project provides a interface to yowsup2. You can Send/Receive Whatsapp-Messages with any language of your choice. 

###Prerequisites:

Install & Configure the yowsup2 CLI Demo. 

Use yowsup-cli to register a Number. 

Install or use a Beanstalkd Server.
 
###Installation(on Ubuntu):

```bash
sudo apt-get install pip3 python3-dev

pip3 install pystalkd

pip3 install git+https://github.com/tgalal/yowsup@master

```


###Configuration:

rename "config.sample.ini" to "config.ini" and put your credentials into it.

###Usage:

Run the Main Handler with:
```
python3 run.py 
```

You will get the Messages from Whatsapp into the Queue "whatsapp-receive".

Put the messages you want to send into the "whatsapp-send" Queue. The Format of the Messages is JSON.

### Integrations in other Languages/Software:

PHP: 
https://github.com/EliasKotlyar/yowsup-queue-php-api


###Example Messages for other Integrations:


Simple Message:

```
	{"type":"simple","body":"This is a Test-Message!","address":"12345678"}
```



###Known Issues:

#### Sometimes the keys are not synced. You will get Errors like this: 
```
	Exception: No such signedprekeyrecord!
```
Fix it using:
```
	rm -r ~/.yowsup/
	(deleted the yowsup database)
```

#### On First Run,its not running well after the generation of the Keys. Please restart it. 

