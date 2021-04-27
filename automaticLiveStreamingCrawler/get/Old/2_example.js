var himalaya = require('himalaya');
var stringSimilarity = require('string-similarity');
var fs = require('fs');

var html1 = fs.readFileSync('HMhtml.txt', {encoding: 'utf8'})
//var html2 = fs.readFileSync('DYhtml2.txt', {encoding: 'utf8'})
var jsonFile1 = himalaya.parse(html1)
//var jsonFile2 = himalaya.parse(html2)

//fs.writeFile("himalayaOrigin.txt", JSON.stringify(jsonFile1));
global.jsonHtml = himalaya.parse(html1)

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

deleteKey(jsonFile1);
//deleteKey(jsonFile2);

fs.writeFile("himalaya1.txt", JSON.stringify(jsonFile1));
//fs.writeFile("himalaya2.txt", JSON.stringify(jsonFile2));

// var similarity = stringSimilarity.compareTwoStrings(JSON.stringify(jsonFile1), JSON.stringify(jsonFile2));
// console.log(similarity);

global.countJson = {};

function countKey(object) {
  for(var property in object) {
    if(property=='value') {
    	if (global.countJson[object[property]] != null){
    		global.countJson[object[property]] = global.countJson[object[property]]+1;
    	}
    	else {
    		global.countJson[object[property]] = 1;
    	}
    	
    } else {
      if(object[property] !== null && typeof object[property] == 'object'){
        countKey(object[property]);
      }
    }
  }
}

countKey(jsonFile1);
console.log("countjson"+JSON.stringify(global.countJson))

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
	console.log("KKKKKK\n\n"+JSON.stringify(count))
	
	for(var number in count) {
		if (number != 1 && count[number] > max && number > 15){
			max = count[number];
		}
		else{
			continue;
		}
	}
	console.log('max:'+max);
	for(var number in count) {
		if (count[number] == max){
			maxNumber = number;
			break;
		}
		else{
			continue;
		}
	}
	console.log(maxNumber);

	for(var need in global.countJson) {
		if(global.countJson[need] == maxNumber){
			desiredKey.push(need);
		}
	}
	return(desiredKey);
}

var desiredKey = needKey();
console.log('DD:'+desiredKey);

global.finalKey = {};

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
				




			// for(var dk in desiredKey){
			// 	//console.log('j = '+desiredKey[dk]);
			// 	if(object['attr'].class == desiredKey[dk]){
			// 		//console.log('HIII')

			// 		global.finalKey[object['attr'].class] = [];
			// 		//console.log(object['attr'])
			// 		for (var j in object['attr']){
			// 			if(j == 'class'){
			// 				//console.log(object['attr'].herf+">>>>>>>>>>>>>>>"+j);
			// 				global.finalKey[object['attr'].class].push('text');
			// 			}
			// 			else{
			// 				global.finalKey[object['attr'].class].push(j);
			// 			}
			// 		}

			// 	}
			// }
		}
		else{
			if(object[i] !== null && typeof object[i] === 'object'){
		        findAttr(object[i], desiredKey);
		    }
		}
	}

	//console.log(finalKey);
	
}

findAttr(global.jsonHtml, desiredKey);
console.log(global.finalKey);

fs.writeFile("finalKey_HM.txt", JSON.stringify(global.finalKey));