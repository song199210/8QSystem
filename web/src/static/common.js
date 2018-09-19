var common=function(){
    return this;
}
common.prototype={
    httpAjax(urlApi,mtype,data){
        var url=`http://localhost:5000/${urlApi}`;
        // var url=`http://119.29.19.43:5000/${urlApi}`;
        return new Promise((resolve,reject)=>{
            fetch(url,{
                method:mtype,
                body:JSON.stringify(data)
            }).then((res)=>{
                resolve(res.json())
            }).catch((err)=>{
                reject(err)
            });
        })
    }
}
export default new common();