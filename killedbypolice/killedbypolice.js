var request = require('request'),
	cheerio = require('cheerio'),
	tableParser = require('cheerio-tableparser'),
	tableRows = [];


request('http://www.killedbypolice.net/', function(err, resp, body){

	if(!err && resp.statusCode == 200){
		var $ = cheerio.load(body);
		var table = $('table');


		// get each tr tag into an array.
		var rowList = []
		$(table).each(function(i, row){
			$(row).find('tr').each(function(i, tr){
					rowList.push(tr);
			});
		});

		

		//iterate through a list of tr tags and find data in each row's td tags
		// with an absolute path.
		for(i=0; i <rowList.length;i++){
			currentRow = rowList[i];
			head = currentRow['children'][0]['children'][0]['children'][0];
			try{
				var date = (head['data']);
				var state = (head['next']['children'][0]['data']);
				var genderrace = (head['next']['next']['children'][0]['data']);
				var method = (head['next']['next']['next']['next']['children'][0]['children'][0]['data']);
				var nameage = (head['next']['next']['next']['children'][0]['data']);

			}catch(err){
				try{
					nameage = (head['next']['next']['next']['children'][0]['children'][0]['data']);
					method = (head['next']['next']['next']['next']['children'][0]['children'][0]['data']);
				}catch(err){

				}
				
				
			}
				
			
			//test contents
			if(date != null){
				console.log(date + '\t\t' + state + '\t\t' + genderrace + '\t\t' + nameage + '\t\t' + method);
			}

			
		}
		

	}
});