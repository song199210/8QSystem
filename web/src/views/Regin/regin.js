import React from "react";
import md5 from "js-md5";
import { Form, Icon, Input, Button, Checkbox,message } from 'antd';
import "./regin.scss";
const FormItem = Form.Item;

var test={
	linkurl: "/testParConfig",
	resourcetitle: "<i class='iconfont iconfont icon-mubanbianpai'></i>检验参数配置",
	childmenu: [{
  	linkurl: "/testParConfig/MaterialCategory",
	  resourcetitle: "<i class='iconfont iconfont icon-mubanbianpai'></i>物资类别",
	},{
  	linkurl: "/testParConfig/TestName",
	  resourcetitle: "<i class='iconfont iconfont icon-mubanbianpai'></i>试验名称",
	},{
  	linkurl: "/testParConfig/InspectionPro",
	  resourcetitle: "<i class='iconfont iconfont icon-mubanbianpai'></i>检验项目",
	},{
  	linkurl: "/testParConfig/InspectionBasis",
	  resourcetitle: "<i class='iconfont iconfont icon-mubanbianpai'></i>检验依据",
	},{
  	linkurl: "/testParConfig/TestRecordTpl",
	  resourcetitle: "<i class='iconfont iconfont icon-mubanbianpai'></i>试验记录模板",
	},{
  	linkurl: "/testParConfig/TestReportpl",
	  resourcetitle: "<i class='iconfont iconfont icon-mubanbianpai'></i>试验报告模板",
	}]
}
class NormalReginForm extends React.Component {
  handleSubmit = (e) => {
    e.preventDefault();
    const _that=this;
    this.props.form.validateFields((err, values) => {
      if (!err) {
        if(values.pwd !== values.pwd2){
          message.error("密码不一致!");
          return false;
        }
        var sendData={
          uname:values["uname"],
          pwd:md5(values["pwd"]),
          email:values["email"]
        }
        window.$common.httpAjax("regin","POST",sendData).then((res)=>{
            if(res.flag === "success"){
              message.success(res.msg);
              _that.props.history.push("email")
            }else{
              message.error(res.msg);
            }
          }).catch((err)=>{
            console.error(err);
          });
      }
    });
  }
  render() {
    const { getFieldDecorator } = this.props.form;
    return (
      <div className="reginBox">
        <div className="container">
          <h3 className="loginTitle">欢迎注册</h3>
          <Form onSubmit={this.handleSubmit} className="login-form">
            <FormItem>
              {getFieldDecorator('uname', {
                rules: [{ required: true, message: '请输入账号!' }],
              })(
                <Input prefix={<Icon type="user" style={{ color: 'rgba(0,0,0,.25)' }} />} placeholder="账号" autoComplete="uname" />
              )}
            </FormItem>
            <FormItem>
              {getFieldDecorator('pwd', {
                rules: [{ required: true, message: '请输入密码!' }],
              })(
                <Input prefix={<Icon type="lock" style={{ color: 'rgba(0,0,0,.25)' }} />} type="password" placeholder="密码" autoComplete="pwd" />
              )}
            </FormItem>
            <FormItem>
              {getFieldDecorator('pwd2', {
                rules: [{ required: true, message: '请输入密码!' }],
              })(
                <Input prefix={<Icon type="lock" style={{ color: 'rgba(0,0,0,.25)' }} />} type="password" placeholder="确认密码" autoComplete="pwd2" />
              )}
            </FormItem>
            <FormItem>
              {getFieldDecorator('email', {
                rules: [{ required: true, message: '请输入邮箱!' }],
              })(
                <Input prefix={<Icon type="mail" style={{ color: 'rgba(0,0,0,.25)' }} />} type="text" placeholder="注册邮箱" autoComplete="email" />
              )}
            </FormItem>
            <FormItem>
              <Button style={{"width":"100%"}} type="primary" htmlType="submit" className="login-form-button">注册</Button>
            </FormItem>
            <div>
              <a className="login-form-forgot" onClick={()=>{this.props.history.push("login")}}>返回登录</a>
            </div>          
          </Form>
        </div>
      </div>
    );
  }
}

const WrappedNormalReginForm = Form.create()(NormalReginForm);

export default WrappedNormalReginForm