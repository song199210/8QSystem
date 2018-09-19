import React from "react";
import { Card, Col, Row,Popconfirm,Button,message } from 'antd';
import "./filmmanager.scss";

class NormalEmailForm extends React.Component {
    constructor(props){
        super(props);
        this.state={
            dataList:[
                {
                    title:"奇迹男孩",
                    director:"蒂芬·卓博斯基",
                    performer:" 雅各布·特伦布莱 / 朱莉娅·罗伯茨",
                    releaseDate:"2018-01-19",
                    score:"8.9",
                    type:"剧情/家庭",
                    timelen:"113分钟"
                },{
                    title:"奇迹男孩",
                    director:"蒂芬·卓博斯基",
                    performer:" 雅各布·特伦布莱 / 朱莉娅·罗伯茨",
                    releaseDate:"2018-01-19",
                    score:"8.9",
                    type:"剧情/家庭",
                    timelen:"113分钟"
                },{
                    title:"奇迹男孩",
                    director:"蒂芬·卓博斯基",
                    performer:" 雅各布·特伦布莱 / 朱莉娅·罗伯茨",
                    releaseDate:"2018-01-19",
                    score:"8.9",
                    type:"剧情/家庭",
                    timelen:"113分钟"
                },{
                    title:"奇迹男孩",
                    director:"蒂芬·卓博斯基",
                    performer:" 雅各布·特伦布莱 / 朱莉娅·罗伯茨",
                    releaseDate:"2018-01-19",
                    score:"8.9",
                    type:"剧情/家庭",
                    timelen:"113分钟"
                },{
                    title:"奇迹男孩",
                    director:"蒂芬·卓博斯基",
                    performer:" 雅各布·特伦布莱 / 朱莉娅·罗伯茨",
                    releaseDate:"2018-01-19",
                    score:"8.9",
                    type:"剧情/家庭",
                    timelen:"113分钟"
                },{
                    title:"奇迹男孩",
                    director:"蒂芬·卓博斯基",
                    performer:" 雅各布·特伦布莱 / 朱莉娅·罗伯茨",
                    releaseDate:"2018-01-19",
                    score:"8.9",
                    type:"剧情/家庭",
                    timelen:"113分钟"
                },{
                    title:"奇迹男孩",
                    director:"蒂芬·卓博斯基",
                    performer:" 雅各布·特伦布莱 / 朱莉娅·罗伯茨",
                    releaseDate:"2018-01-19",
                    score:"8.9",
                    type:"剧情/家庭",
                    timelen:"113分钟"
                }
            ]
        }
    }
    handleSubmit = (e) => {
        e.preventDefault();
    }
    componentDidMount(){
        // this.queryDataList(1);
    }
    onSearchCode(key){
        
    }
    queryDataList=()=>{
        const values={
            keyStr:"",
            userid:window.localStorage.getItem("userId")
        }
        const _that=this;
        window.$common.httpAjax("codemanager/query","POST",values).then((res)=>{
            if(res.flag === "success"){
                _that.setState({
                    dataList:res.data
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
        const {dataList}=this.state;
        const cardList=dataList.map((item,index)=>{
            return (
                <Col span={3} key={index}>
                    <Card title={item.c_title} bordered={false}>
                        <p className="code_desc"><img src={require('@/src/static/images/1213.jpg')} alt/></p>
                        <p style={{margin:"0px",textAlign:"center"}}><a href="">{item.title}（{item.score}）</a></p>
                    </Card>
                </Col>
            );
        })
        return (
            <div>
                <div className="searContainer" style={{marginBottom:"10px"}}>
                    <div className="right_add" style={{textAlign:"right"}}>
                        <Button type="primary" onClick={()=>this.setData("add")}>开始爬取</Button>
                    </div>
                </div>
                <div className="filmBox" style={{ background: '#ECECEC', padding: '20px'}}>
                    <Row gutter={16}>{cardList}</Row>
                </div>
            </div>
        );
    }
}

export default NormalEmailForm