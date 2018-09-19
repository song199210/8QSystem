import React from "react";
import md5 from "js-md5";
import { Form, Icon, Input, Button, Checkbox,message } from 'antd';
import "./login.scss";
const FormItem = Form.Item;
const storage=window.localStorage;
class NormalLoginForm extends React.Component {
  constructor(props){
    super(props)
    this.state={
      isChk:true
    }
  }
  componentDidMount(){
    this.props.form.setFieldsValue({
      "uname":storage.getItem("uname")?storage.getItem("uname"):"",
      "pwd":storage.getItem("pwd")?storage.getItem("pwd"):""
    })
  }
  handleSubmit = (e) => {
    e.preventDefault();
    const {form,history}=this.props;
    const {isChk}=this.state;
    form.validateFields((err, values) => {
      if(isChk){//保存账号密码
        storage.setItem("uname",values.uname);
        storage.setItem("pwd",values.pwd);
      }else{//不保存账号密码
        storage.removeItem("uname");
        storage.removeItem("pwd");
      }
      values.pwd=md5(values.pwd);
      if (!err) {
        window.$common.httpAjax("login/islogin","POST",values).then((res)=>{
                if(res.flag === "success"){
                  message.success(res.msg);
                  storage.setItem("userId",res.data.userid);
                  storage.setItem("menulist",JSON.stringify(res.data.menus));
                  history.push("/admin");
                }else{
                  message.error(res.msg);
                }
              }).catch((err)=>{
                console.error(err);
              });
      }
    });
  }
  rUserInfo=(evt)=>{
    const tar=evt.target;
    this.setState({
      isChk:tar.checked
    })
  }
  render() {
    const { getFieldDecorator } = this.props.form;
    const {isChk} = this.state;
    return (
      <div className="loginBox">
        <div className="container">
          <h3 className="loginTitle">欢迎登录</h3>
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
              {getFieldDecorator('remember', {
                valuePropName: 'checked',
                initialValue: isChk,
              })(
                <Checkbox onChange={(evt)=>{this.rUserInfo(evt)}}>记住密码</Checkbox>
              )}
              <div>
                <Button style={{"width":"100%"}} type="primary" htmlType="submit" className="login-form-button">登录</Button>
              </div>
            </FormItem>
            <div>
              <a className="login-form-forgot" onClick={()=>{this.props.history.push("setpwd")}}>忘记密码</a> Or <a onClick={()=>{this.props.history.push("regin")}}>去注册!</a>
            </div>          
          </Form>
        </div>
      </div>
    );
  }
}

const WrappedNormalLoginForm = Form.create()(NormalLoginForm);

export default WrappedNormalLoginForm