import React from "react";
import {HashRouter as Router,Switch,Route,Link,Redirect} from "react-router-dom";

import HeaderView from "../../components/header/header";
import SiderbarView from "../../components/sidebar/sidebar";

import FilmManager from "../filmManager/filmmanager";
import MusicManager from "../musicManager/musicmanager";
import JokeManager from "../jokeManager/jokemanager";
import Photography from "../Photography/Photography";
import "./admin.scss";

const storage=window.localStorage;
class NormalAdminComponent extends React.Component {
    constructor(props){
        super(props);
    }
    render(){
        const menulist=JSON.parse(storage.getItem("menulist"));
        const {match,history}=this.props;
        if(menulist && menulist.length>0){
            var routeJSX=menulist.map((item,index)=>{
                var url=`${match.path}/${item.url}`;
                var component=null;
                if(item.url === "films"){
                    component=FilmManager;
                }else if(item.url === "musics"){
                    component=MusicManager;
                }else if(item.url === "jokes"){
                    component=JokeManager;
                }else if(item.url === "photography"){
                    component=Photography
                }
                return <Route component={component} key={index} path={url} />
            })
        }
        const el=(
            <div className="adminBox">
                <HeaderView></HeaderView>
                <SiderbarView history={history} match={match}></SiderbarView>
                <div className="c_box">
                    <Router>
                        <Switch>
                            {routeJSX}
                        </Switch>
                    </Router>
                </div>
            </div>
        );
        return el;
    }
}

export default NormalAdminComponent;