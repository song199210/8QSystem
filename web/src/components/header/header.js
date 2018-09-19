import React from "react";
import "./header.scss";

class NormalHeader extends React.Component {
    constructor(props){
        super(props);
        this.state={
            datetime:this.formatDateTime(new Date())
        }
    }
    componentDidMount(){
        this.cDateTime();
    }
    formatDateTime=(dateTime)=>{
        let year=dateTime.getFullYear(),
            month=dateTime.getMonth(),
            date=dateTime.getDate(),
            hours=dateTime.getHours(),
            minutes=dateTime.getMinutes(),
            seconds=dateTime.getSeconds();
        month=month<10?`0${month.toString()}`:month.toString();
        date=date<10?`0${date.toString()}`:date.toString();
        hours=hours<10?`0${hours.toString()}`:hours.toString();
        minutes=minutes<10?`0${minutes.toString()}`:minutes.toString();
        seconds=seconds<10?`0${seconds.toString()}`:seconds.toString();
        return `${year}-${month}-${date} ${hours}:${minutes}:${seconds}`;
    }
    cDateTime(){
        var _that=this;
        setInterval(()=>{
            _that.setState({
                datetime:_that.formatDateTime(new Date())
            });
        },1000);
    }
    render(){
        let {datetime}=this.state;
        let el=(
            <div className="header">
                <div className="leftBox">
                    <h2>代码管理系统</h2>
                </div>
                <div className="rightBox">
                    <span><img src={require('../../static/images/userImg.jpg')} alt="头像"/></span>
                    <span>{datetime}</span>
                    <span>退出登录</span>
                </div>
            </div>
        );
        return el;
    }
}

export default NormalHeader;