import React, { Component } from 'react';
import {HashRouter as Router,Switch,Route,Link,Redirect} from "react-router-dom";
import common from "./static/common";
import LoginForm from "./views/Login/login";
import ReginForm from "./views/Regin/regin";
import EmailForm from "./views/Regin/email";
import AdminComponent from "./views/admin/admin";
import TestComponent from "./views/Test/test";
window.$common=common;

class App extends Component {
  constructor(props){
    super(props)
  }
  render() {
    return (
      <div className="App">
        <Router>
          <Switch>
            <Route component={TestComponent} path="/test" exact={true}/>
            <Route component={LoginForm} path="/login" exact={true}/>
            <Route component={ReginForm} path="/regin"/>
            <Route component={EmailForm} path="/email"/>
            <Route component={AdminComponent} path="/admin"/>
            <Route path="/" render={()=><Redirect to='login'/>} />
          </Switch>
        </Router>
      </div>
    );
  }
}

export default App;
