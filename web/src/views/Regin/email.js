import React from "react";
import { Form, Icon, Input, Button, Checkbox,message } from 'antd';
import "./regin.scss";

class NormalEmailForm extends React.Component {
  handleSubmit = (e) => {
    e.preventDefault();
  }
  render() {
    return (
      <div className="emailBox">
        <div className="container">
          <h3 className="loginTitle">注册成功</h3>
          注册成功，请立即去<a href="javascript:void(0);">【注册邮箱:1821908096@qq.com】</a>激活该账号！
        </div>
      </div>
    );
  }
}

export default NormalEmailForm