import React from "react";
import { Card, Col, Row,Popconfirm,Button,message } from 'antd';
import "./musicmanager.scss";

const ButtonGroup=Button.Group;
class NormalEmailForm extends React.Component {
    constructor(props){
        super(props);
        this.state={
            dataList:[
                {
                    title:"奇迹男孩",
                    director:"蒂芬·卓博斯基",
                    num:"3012次播放"
                },{
                    title:"奇迹男孩",
                    director:"蒂芬·卓博斯基",
                    num:"3012次播放"
                },{
                    title:"奇迹男孩",
                    director:"蒂芬·卓博斯基",
                    num:"3012次播放"
                },{
                    title:"奇迹男孩",
                    director:"蒂芬·卓博斯基",
                    num:"3012次播放"
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
        console.log(row)
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
                <Col span={6} key={index}>
                    <Card title={item.c_title} bordered={false}>
                        <div className="music_item">
                            <span className="music_img"><img src="" alt="" /></span>
                            <span className="music_info">
                                <h4>{item.title}</h4>
                                <p>{item.director}/{item.num}</p>
                            </span>
                            <div className="btn_group">
                                <ButtonGroup>
                                    <Button icon="cloud" />
                                    <Popconfirm title="确认删除?" onConfirm={()=>{this.deleteData(item)}} okText="确定" cancelText="取消">
                                        <Button type="danger" icon="cloud-download" />
                                    </Popconfirm>
                                </ButtonGroup>
                            </div>
                        </div>
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
                <div className="musicBox" style={{ background: '#ECECEC', padding: '20px'}}>
                    <Row gutter={16}>{cardList}</Row>
                </div>
            </div>
        );
    }
}

export default NormalEmailForm