function con(){
    var message = confirm("確認刪除嗎？");
    if(message){
        return true;
    }else{
        return false;
    }
}