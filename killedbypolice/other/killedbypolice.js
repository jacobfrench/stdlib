var request = require('request'),
	cheerio = require('cheerio'),
	tableParser = require('cheerio-tableparser'),
	fs = require('fs'),
	readline = require('readline');
	// tableRows = [];

function getDate(line){
			var date = '';
			var months = ['January', 'February', 'March',
					  'April', 'May', 'June', 'July',
					  'August', 'September', 'October',
					  'November', 'December'
					 ];
			for(i=0; i<line.length; i++){
				for(j=0; j<months.length; j++){
					if(line[i].indexOf(months[j])  > -1){
						date = months[j] + ' ' + line[i+1];
					}
				}
			}
			return date;
		};


request('http://www.killedbypolice.net/kbp2013.html', function(err, resp, body){



	if(!err && resp.statusCode == 200){
		var $ = cheerio.load(body);
		var table = $('table');
		var rawText = (table.text());



		// write raw text to out.txt
		// fs.writeFile('out.txt', rawText, function(err){
		// 	if(err) throw err;
		// 	// console.log(rawText + '> out.txt');
			
		// });




		var fileContents = fs.readFileSync('out.txt');
		var lines = fileContents.toString().split('\n');

		//split strings in lines to create an array
		// with each line in a seperate array element.
		var arr = []
		for(var i=0; i < lines.length; i++){
			if(lines[i] != '')
				arr.push(lines[i].split('\n'));
		}


		var month = '';
		var day = '';
		



		


		for(i=0; i<arr.length; i++){
			var splitStrArray = arr[i].toString().split(' ');
			var date = getDate(splitStrArray);
			if(date.length < 16 && date != '')
				console.log(i+ ' ' + date)
			// console.log(splitStrArray)



			// if(splitStr[0].indexOf('facebook') > -1){
			// 	splitStr[0] = '--';
			// 	console.log(splitStr);
			// }
			// else{
			// 	console.log(splitStr);
			// }
		}
		
		
		// for(i=0; i< arr.length; i++){
		// 	console.log(arr[i]);
		// }

















		// var tdlist = []
		// $(table).each(function(i, row){
		// 	$(row).find('td').each(function(i, td){
		// 			tdlist.push(td);



		// 	});

		// });


		// // start iterating from 22 and move 7 for each iteration.
		// // this works when the name field is either empty or has only
		// // a string with no link in the name field.
		// var i = 8;
		// // console.log('========================================================')
		// // console.log(list[i]['children'][0]['children'][0]);
		// // console.log('========================================================')
		// var date = '';
		// var state = '';
		// var gender = '';
		// var name = '';
		// var method = '';

		// try{
			// each tr contains 7 td tags.
			// this works when the name field is either empty or has only
			// a string with no link in the name field. 
			//TODO: change these to iterate through a list of rows rather than a list of td tags.
			// date = (tdlist[i]['children'][0]['children'][0]['data']); //date
			// state = (tdlist[i]['children'][0]['children'][0]['next']['children'][0]['data']); //state
			// gender = (tdlist[i]['children'][0]['children'][0]['next']['next']['children'][0]['data']); //gender/race
			// name = (tdlist[i]['children'][0]['children'][0]['next']['next']['next']['children'][0]['data']); //name/age
			// method = (tdlist[i]['children'][0]['children'][0]['next']['next']['next']['next']['children'][0]['children'][0]['data']); //method
		// }catch(err){
			// this works when the name field is either empty or has
			// a string WITH a link in the name field.
			// date = (tdlist[i]['children'][0]['children'][0]['data']); //date
			// state = (tdlist[i]['children'][0]['children'][0]['next']['children'][0]['data']); //state
			// gender = (tdlist[i]['children'][0]['children'][0]['next']['next']['children'][0]['data']); //gender/race
			// method = (tdlist[i]['children'][0]['children'][0]['next']['next']['next']['children'][0]['children'][0]['data']); //name/age
			// console.log(tdlist[i]['children'][0]['children'][0]['next']['next']['next']['children']); //method

		// }
			

		// console.log(date);
		// console.log(state);
		// console.log(gender);
		// console.log(name);
		// console.log(method);

		// // works when name field also contains a link
		// console.log(list[i]);
		// console.log('============================')
		// console.log(list[i]['children'][0]['children'][0]['data']); //date
		// console.log(list[i]['children'][0]['children'][0]['next']['children'][0]['data']); //state
		// console.log(list[i]['children'][0]['children'][0]['next']['next']['children'][0]['data']); //gender/race
		// console.log(list[i]['children'][0]['children'][0]['next']['next']['next']['children'][0]['children'][0]['data']); //name/age
		// console.log(list[i]['children'][0]['children'][0]['next']['next']['next']['children']); //method

		
		

	}
});