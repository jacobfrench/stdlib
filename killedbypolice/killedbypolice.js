var request = require('request'),
	cheerio = require('cheerio'),
	tableParser = require('cheerio-tableparser'),
	tableRows = [];

function cleanDate(date){
	var cleanedDate = '';
	var sections = date.split(' ');
	return sections[1] + ' ' + sections[2] + ' ' + sections[3];
}

function cleanGenderRace(genderRace){
	var sections = genderRace.split('/');
	if(sections.length < 2){
		sections.push('');
	}
	return sections;

}



request('http://www.killedbypolice.net/', function(err, resp, body){

	if(!err && resp.statusCode == 200){
		var $ = cheerio.load(body);
		var table = $('table');


		// get each tr tag into an array.
		var rowList = [];
		$(table).each(function(i, row){
			$(row).find('tr').each(function(i, tr){
					rowList.push(tr);
			});
		});

		

		//iterate through a list of tr tags and find data in each row's td tags
		// with an absolute path.
		for(i=0; i<rowList.length; i++){
			var currentRow = rowList[i];
			var head = currentRow.children[0].children[0].children[0];
			try{
				var date = (head.data);
				var state = (head.next.children[0].data);
				var genderRace = (head.next.next.children[0].data);
				var method = (head.next.next.next.next.children[0].children[0].data);
				var nameage = (head.next.next.next.children[0].data);

			}catch(err){
				try{
					nameage = (head.next.next.next.children[0].children[0].data);
					method = (head.next.next.next.next.children[0].children[0].data);
				}catch(err){
				}
				
				
			}
			

			//test contents
			if(date != null){
				var gender = cleanGenderRace(genderRace)[0];
				var race = cleanGenderRace(genderRace)[1];
				console.log(cleanDate(date) + '\t\t' + state + '\t\t' + gender + '\t\t' 
					+ race + '\t\t' + nameage + '\t\t' + method);
			}

			
		}
		
	}
});