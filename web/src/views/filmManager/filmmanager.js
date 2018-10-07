import React from "react";
import { Card, Col, Row,Popconfirm,Button,message } from 'antd';
import FilmDetailModal from "./filmDetailModal";
import "./filmmanager.scss";

class NormalEmailForm extends React.Component {
    constructor(props){
        super(props);
        this.lmore_dom=null;
        this.child_com=null;
        this.state={
            visible:false,
            pageno:1,
            dataList:[]
        }
    }
    handleSubmit = (e) => {
        e.preventDefault();
    }
    componentDidMount(){
        const {pageno}=this.state;
        this.queryDataList(pageno);
    }
    loadmorefuns=(evt)=>{
        const {pageno}=this.state;
        this.queryDataList(pageno+1);
    }
    openModal=(type,data)=>{
        this.setState({
            visible:true
        });
        this.child_com.initDetailJson(data);
    }
    handleClose=()=>{
        this.setState({
            visible:false
        });
    }
    onRef=(child)=>{
        this.child_com=child;
    }
    queryDataList=(pageno)=>{
        const values={
            userid:window.localStorage.getItem("userId")
        }
        const _that=this;
        const sendData={
            pageno:pageno,
            pagesize:16
        }
        const data_list=this.state.dataList;
        window.$common.httpAjax("film/query","POST",sendData).then((res)=>{
            if(res.flag === "success"){
                if(res.data.length == 0){
                    if(_that.lmore_dom != null){
                        _that.lmore_dom.innerHTML="加载完毕"
                    }
                    return false;
                }
                _that.setState({
                    dataList:[].concat(data_list,res.data),
                    pageno:pageno
                });
            }else{
                message.error(res.msg);
            }
        }).catch((err)=>{
            console.error(err);
        });
    }
    setData=(type)=>{
        if(type === "add"){
            const url=`${this.props.match.path}/add`;
            this.props.history.push(url);
        }
    }
    editData=(row)=>{
        const {history}=this.props;   
        window.localStorage.setItem("codeDetail",JSON.stringify(row));
        history.push("codemanager/update");
    }
    deleteData=(row)=>{
        const values={
            c_id:row.id,
            userid:window.localStorage.getItem("userId")
        }
        const _that=this;
        window.$common.httpAjax("codemanager/delete","POST",values).then((res)=>{
            if(res.flag === "success"){
                message.success(res.msg);
                _that.queryDataList();
            }else{
                message.error(res.msg);
            }
        }).catch((err)=>{
            console.error(err);
        });
    }
    render() {
        const {visible,dataList}=this.state;
        const cardList=dataList.map((item,index)=>{
            var imgurl=`http://localhost:5000${item.fimgurl}`;
            var ftypelist=item.type.split("/");
                ftypelist.splice(2);
            var ftype=ftypelist.join("/");
            return (
                <Col span={3} key={index}>
                    <Card title={item.c_title} bordered={false}>
                        <p className="code_desc"><img src={imgurl} alt=""/></p>
                        <p style={{margin:"0px",textAlign:"center",height:"21px",overflow:"hidden"}}><a href="javascript:void(0);" onClick={()=>this.openModal('add',item)}>{item.title}</a></p>
                        <p style={{margin:"0px",textAlign:"center",height:"21px"}}>{ftype}<b>（{item.score}）</b></p>
                    </Card>
                </Col>
            );
        })
        return (
            <div style={{height:"100%"}}>
                <div className="searContainer" style={{marginBottom:"10px"}}>
                    <div className="right_add" style={{textAlign:"right"}}>
                        <Button type="primary" onClick={()=>this.setData("add")}>开始爬取</Button>
                    </div>
                </div>
                <div className="filmBox" style={{ background: '#ECECEC', padding: '20px'}}>
                    <Row gutter={16}>{cardList}</Row>
                    <div style={{textAlign:"center"}}><button className="loadmore" onClick={this.loadmorefuns} ref={(dom)=>this.lmore_dom=dom}>加载更多</button></div>
                </div>
                <FilmDetailModal visible={visible} closeModal={this.handleClose} onRef={this.onRef}></FilmDetailModal>
            </div>
        );
    }
}

export default NormalEmailForm