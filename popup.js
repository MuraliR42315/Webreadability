  chrome.tabs.query({'active': true, 'lastFocusedWindow': true}, function (tabs) {
     var url = tabs[0].url;
     create(url);
	
});
function create(a){
  a=a.replace("https","http");
    $.ajax({
        url:'http://127.0.0.1:5000/download',
        data:{
          url:a, 'status':'check'
        },
        type:"POST",
        dataType:"json",
	success: function(data) {
                                        var read = parseInt(data[0])
					console.log(read)
					if (read==0)
						$('#text1').val("Less Readable")
					else if (read==1)
						$('#text1').val("Readable")
					else
						$('#text1').val("Highly Readable")
                                    	var grade=parseInt(data[1])
					if (grade==0)
						$('#text2').val("5th Grade")
					else if (grade==1)
						$('#text2').val("6th Grade")
					else if (grade==2)
						$('#text2').val("7th Grade")
					else if (grade==3)
						$('#text2').val("8 & 9th Grade")
					else if (grade==4)
						$('#text2').val("10 & 12th Grade")
					else if (grade==5)
						$('#text2').val("College Grade")
					else
						$('#text2').val("Graduate")
					
					console.log(data)
                                        //chrome.runtime.sendMessage({type: "isStatus", count: data});
                                        data = null;
                                     },	 
		
    });
}
