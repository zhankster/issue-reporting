function currentDate() {
    let today = new Date();
    let dd = today.getDate();

    let mm = today.getMonth()+1; 
    const yyyy = today.getFullYear();
    if(dd<10) 
    {
        dd=`0${dd}`;
    } 

    if(mm<10) 
    {
        mm=`0${mm}`;
    } 
    today = `${yyyy}-${mm}-${dd}`;

    return today;
}

function pad(num){
    var s = "" + num;
    if ( num < 10 ) {
      s = "0" + num; 
    }
    return s;
}

function removeLeading(num) {
    return num.replace(/^(0+)/g, '')
}

function changeDateFormat(inputDate){  // expects Y-m-d
    var splitDate = inputDate.split('-');
    if(splitDate.count == 0){
        return null;
    }

    var year = splitDate[0];
    var month = removeLeading(splitDate[1]);
    var day = removeLeading(splitDate[2]); 

    return month + '/' + day + '/' + year;
}

function dateCompare(dtmfrom, dtmto){
    return new Date(dtmfrom).getTime() >=  new Date(dtmto).getTime() ;
 }

