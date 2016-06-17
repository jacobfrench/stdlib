var request = require('request'),
	cheerio = require('cheerio'),
	tableParser = require('cheerio-tableparser'),
	tableRows = [];


request('http://www.killedbypolice.net/kbp2013.html', function(err, resp, body){





	if(!err && resp.statusCode == 200){
		var $ = cheerio.load(body);
		var table = $('table');


		var tdlist = []
		$(table).each(function(i, row){
			$(row).find('td').each(function(i, td){
					tdlist.push(td);
					// console.log(td['children'][0]['children'][0]['data']); //date


				
				
			});

		});

		// start iterating from 22 and move 7 for each iteration.
		// this works when the name field is either empty or has only
		// a string with no link in the name field.
		var i = 8;
		// console.log(list[i]);
		// console.log('========================================================')
		// console.log(list[i]['children'][0]['children'][0]);
		// console.log('========================================================')
		var date = '';
		var state = '';
		var gender = '';
		var name = '';
		var method = '';


		try{
			date = (tdlist[i]['children'][0]['children'][0]['data']); //date
			state = (tdlist[i]['children'][0]['children'][0]['next']['children'][0]['data']); //state
			gender = (tdlist[i]['children'][0]['children'][0]['next']['next']['children'][0]['data']); //gender/race
			name = (tdlist[i]['children'][0]['children'][0]['next']['next']['next']['children'][0]['data']); //name/age
			method = (tdlist[i]['children'][0]['children'][0]['next']['next']['next']['next']['children'][0]['children'][0]['data']); //method
		}catch(err){
			date = (tdlist[i]['children'][0]['children'][0]['data']); //date
			state = (tdlist[i]['children'][0]['children'][0]['next']['children'][0]['data']); //state
			gender = (tdlist[i]['children'][0]['children'][0]['next']['next']['children'][0]['data']); //gender/race
			method = (tdlist[i]['children'][0]['children'][0]['next']['next']['next']['children'][0]['children'][0]['data']); //name/age
			// console.log(tdlist[i]['children'][0]['children'][0]['next']['next']['next']['children']); //method

		}
			

		

		console.log(date);
		console.log(state);
		console.log(gender);
		console.log(name);
		console.log(method);

		



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