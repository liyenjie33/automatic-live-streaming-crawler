var http = require('http');
var url = require('url');
var util = require('util');
var express = require('express');
var cors = require('cors');
var app = express();
var querystring = require('querystring');
var fs = require('fs');
var himalaya = require('himalaya');
var stringSimilarity = require('string-similarity');


global.keyHtml = {
	"nodeDesired_DY":"https://www.douyu.com/directory/all", 
	"nodeDesired_BL":"https://live.bilibili.com/all",
	"nodeDesired_HY":"https://www.huya.com/l",
	"nodeDesired_ZQ":"https://www.zhanqi.tv/lives",
	"nodeDesired_HJ":"https://www.huajiao.com/category/1000",
	"nodeDesired_EG":"https://egame.qq.com/livelist",
	"nodeDesired_IK":"http://www.inke.cn/hotlive_list.html",
	"nodeDesired_TC":"https://www.twitch.tv/directory/all",
	"nodeDesired_YT":"https://www.youtube.com/",
	"nodeDesired_MX":"https://mixer.com/browse/all"
}


function deleteKey(object) {
	var value = 0;
  	for(var property in object) {
	    if (isNaN(parseInt(property, 10))) {

	    	if(property !== 'children' && property !== 'tagName' && property !== 'attributes' && property !== 'type') {
		    	if(property == 'key'){
		    	 	if(object[property] !== 'class'){
		    	 		delete object[property];
		    	 	}
		    	 	else{
		    	 		value = 1;
		    	 		continue;
		    	 	}
		    	}
		    	else if(property == 'value'){
		    		if (value == 1){
		    			continue;
		    		}
		    		else{
		    			delete object[property];
		    		}
		    	}
		    	else{
		    		delete object[property];
		    	}
		    } 
		    else {
			    if(object[property] !== null && typeof object[property] === 'object'){
			        deleteKey(object[property]);
			    }
		    }
	    }
	    else {
	    	if(object[property] !== null && typeof object[property] === 'object'){
			    deleteKey(object[property]);
			}
	    }

 	}
}
function countKey(object) {
  for(var property in object) {
    if(property=='value') {

    	if(object[property].includes("hidden")){
    		//console.log(object[property]+"     "+temp)

    		var temp = object[property].replace(" hidden","")
    		//console.log(object[property]+"     "+temp)
    		if (global.countJson[temp] != null){
	    		global.countJson[temp] = global.countJson[temp]+1;
	    	}
	    	else {
	    		global.countJson[temp] = 1;
	    	}
    	}
    	else{
    		if (global.countJson[object[property]] != null){
	    		global.countJson[object[property]] = global.countJson[object[property]]+1;
	    	}
	    	else {
	    		global.countJson[object[property]] = 1;
	    	}
    	}
	   

    	
    } else {
      if(object[property] !== null && typeof object[property] == 'object'){
        countKey(object[property]);
      }
    }
  }
}
function needKey(){
	var desiredKey = new Array(); //all desired key
	var count = {};  //which number shows most frequency
	var max = 0;
	var maxNumber;
	for(var property in global.countJson){
		if(count[global.countJson[property]] != null){
			count[global.countJson[property]] = count[global.countJson[property]] + 1;
		}
		else{
			count[global.countJson[property]] = 1;
		}
	}
	// console.log("KKKKKK\n\n"+JSON.stringify(count))
	
	for(var number in count) {
		if (number != 1 && count[number] > max && number >10){
			max = count[number];
		}
		else{
			continue;
		}
	}
	//console.log('max:'+max);
	for(var number in count) {
		if (count[number] == max && number > 8){
			maxNumber = number;
			break;
		}
		else{
			continue;
		}
	}
	// console.log(maxNumber);

	for(var need in global.countJson) {
		if(global.countJson[need] == maxNumber && need!=""){
			desiredKey.push(need);
		}
	}
	return(desiredKey);
}
function findAttr(object, desiredKey){
	for(var i in object) {
		
		if(i == 'attributes'){

			for (var j in object['attributes']){
				if (object['attributes'][j]['key']=='class'){
					for(var dk in desiredKey){
						if (object['attributes'][j]['value']==desiredKey[dk]){
							var Class = object['attributes'][j]['value']
							Class = Class.replace(/ /g, ",");
							global.finalKey[Class] = [];

							for(var k in object['attributes']){
								 if(object['attributes'][k]['key']=='class'){
								 	global.finalKey[Class].push('text');
								 }
								 else{
								 	global.finalKey[Class].push(object['attributes'][k]['key']);
								 }
							}
							break;
						}
						else{
							continue;
						}
					}
				}
			}
				

		}
		else{
			if(object[i] !== null && typeof object[i] === 'object'){
		        findAttr(object[i], desiredKey);
		    }
		}
	}
	
}


app.use(cors());

app.get('/test', function(req, res) {

        var params = url.parse(req.url, true).query;

        if (params.reget == 'no') {
        	var nodeDesired = fs.readFileSync(params.name+'.txt', {encoding: 'utf8'})
        	res.write(nodeDesired);
        	res.end();
        }
        if (params.reget == 'yes') {
        	var webdriver = require('selenium-webdriver'),
				By = webdriver.By,
				until = webdriver.until;

			var driver = new webdriver.Builder()
				.forBrowser('chrome')
				.build();

			const sleep = (milliseconds) => {
				return new Promise(resolve => setTimeout(resolve, milliseconds))
			}

			driver.get(global.keyHtml[params.name]).then(function(){
				const sleep = (milliseconds) => {
					return new Promise(resolve => setTimeout(resolve, milliseconds))
				}
			    sleep(5000).then(() => {
					
				
					driver.getPageSource().then(function(html1) {
						var jsonFile1 = himalaya.parse(html1)
				        global.jsonHtml = himalaya.parse(html1)
				        deleteKey(jsonFile1);
				        global.countJson = {};
				        countKey(jsonFile1);
				        console.log(global.countJson)
				        var desiredKey = needKey();
				        console.log(desiredKey)
				        global.finalKey = {};
				        findAttr(global.jsonHtml, desiredKey);
				        console.log(global.finalKey)

				        global.info1 = {};
				        global.info2 = {};

				        async function RemoveRepeat() {
				        	for(var k=0; k<2; k++){
					        	for(var i in global.finalKey) {
					        		var first = i;
					        		var channels = await driver.findElements(By.css("."+first));
					        		
					       			var name = '';
					       			var TAG = '';
					       			for(var tag in global.finalKey) {
					       				if (tag ==first) {
					       					continue;
					       				}
					       				else {
					       					name = tag;
				        					TAG = tag;
				        					if (tag.search(",")!= -1) {
				        						TAG = tag.replace(/,/g, ".");
				        						if (TAG.substr((TAG.length)-1)=="."){
				        							TAG = TAG.substr(0,(TAG.length)-1);
				        						}
				        					}
				        					try{
				        						var temp = await channels[k].findElement(By.css("."+TAG));
				        					}
				        					catch(e){
				        						var temp = ""
				        					}
				        					for (var content = 0;content< global.finalKey[tag].length;content++) {
				        						if (global.finalKey[tag][content] == 'text') {
				        							try {
				        								var TEXT = await temp.getText();
				        								if (k == 0) {
				        									global.info1[name+'_'+global.finalKey[tag][content]] = TEXT;
				        								}
				        								else {
				        									global.info2[name+'_'+global.finalKey[tag][content]] = TEXT;
				        								}
					        								
				        							}
				        							catch(e) {
				        								continue;
				        							}
				        						}
				        						else{
				        							try {
				        								var attr = await temp.getAttribute(finalKey[tag][content]);
				        								if (k == 0) {
				        									global.info1[name+'_'+global.finalKey[tag][content]] = attr;
				        								}
				        								else {
				        									global.info2[name+'_'+global.finalKey[tag][content]] = attr;
				        								}
				        							}
				        							catch(e) {
				        								continue;
				        							}
				        						}
				        					}
				        				}
				        			}
					        		break;
					        	}
					        }
					        console.log(JSON.stringify(global.info1))
					        console.log(JSON.stringify(global.info2))
					        for(var key in global.info1){
					        	if (global.info1[key]==global.info2[key]) {
					        		delete global.info1[key];
					        		delete global.info2[key];
					        	}
					        	else if (global.info1[key].search('\n')!=-1) {
					        		delete global.info1[key];
					        		delete global.info2[key];
					        	}
					        	else {
					        		continue;
					        	}
					        }
					        console.log(JSON.stringify(global.info1))
					        console.log(JSON.stringify(global.info2))
					        
					        var CT = []
					        for(var y in global.info1){
					        	if (CT==[]) {
					        		CT.push(global.info1[y]);
					        	}
					        	else{
					        		var ct = 0;
					        		for(var g in CT){
					        			ct=ct+1;
					        			if (CT[g]==global.info1[y]) {

					        				delete global.info1[y];
					        				break;
					        			}
					        		}
					        		if (ct==CT.length) {
					        			CT.push(global.info1[y]);
					        		}
					        	}
					        }

					        var tag;
					        var config = {}
					        for(var fn in global.info1){
					        	if (global.info1[fn].search('http')!=-1) {
					        		if ((global.info1[fn].search('jpg')!=-1) || (global.info1[fn].search('png')!=-1) || (global.info1[fn].search('JPG')!=-1) ||(global.info1[fn].search('PNG')!=-1)) {
					        			tag = fn.split('_');
					        			config['image'] = tag;
					        		}
					        		else{
					        			tag = fn.split('_');
					        			config['url'] = tag;
					        		}
					        	}
					        	// console.log(">>"+global.info1[fn]+"<<")
					        	// console.log(isNaN(global.info1[fn]))
					        	else if ((global.info1[fn].search('万')!=-1) || (isNaN(global.info1[fn])==false) || (global.info1[fn].search('人')!=-1)) {
					        		if ((global.info1[fn]=="") || (global.info1[fn]==" ")) {
					        			continue;
					        		}
					        		else if (global.info1[fn].search('人')!=-1) {
					        			var a = global.info1[fn].replace(/人/g, '')
					        			if (isNaN(a)==false) {
					        				tag = fn.split('_');
					        				config['viewer'] = tag;
					        			}
					        		}
					        		else {
					        			tag = fn.split('_');
					        			config['viewer'] = tag;
					        		}
					        	}
					        	else if ((fn.search('title')!=-1) || (fn.search('TITLE')!=-1) || (fn.search('Title')!=-1) || (fn.search('livename')!=-1) || (fn.search('intro')!=-1) || (fn.search('room-name')!=-1)){
					        		tag = fn.split('_');
					        		config['title'] = tag;
					        	}
					        	else if ((fn.search('user')!=-1) || (fn.search('username')!=-1) || (fn.search('anchor')!=-1) || (fn.search('uname')!=-1) || (fn.search('avator')!=-1) || (fn=="name,fl_text") ) {
					        		tag = fn.split('_');
					        		config['host'] = tag;
					        	}
					        	else if ((fn.search('zone')!=-1) || (fn.search('type')!=-1) || (fn.search('game-name')!=-1)) {
					        		tag = fn.split('_');
					        		config['category'] = tag;
					        	}
					        	else{
					        		tag = fn.split('_');
					        		config[fn] = tag;
					        	}
					        	console.log(config)
					        }
					        config['block'] = first;
					        console.log(config);
					        res.write(JSON.stringify(config));
        					res.end();
					        await fs.writeFile(params.name+".txt", JSON.stringify(config));
					        driver.quit();

				        }
				        const sleep = (milliseconds) => {
							return new Promise(resolve => setTimeout(resolve, milliseconds))
						}
				        sleep(5000).then(() => {
						  RemoveRepeat();
						});
				        


					})
				});

			});
	
        } //if end
});

app.get('/', function(req, res) {
	res.send('KKKK');
});

app.listen(3000, function () {
        console.log('listening on port 3000!')
});

