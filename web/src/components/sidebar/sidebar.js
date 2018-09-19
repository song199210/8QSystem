import React from "react";
import { Menu, Icon } from 'antd';
import "./sidebar.scss";

const storage=window.localStorage;
const SubMenu = Menu.SubMenu;
const MenuItemGroup = Menu.ItemGroup;

class SiderbarComponent extends React.Component {
    constructor(props){
        super(props)
    }
    handleClick = (e) => {
        if(e.key){
            const url=`${this.props.match.path}/${e.key}`;
            this.props.history.push(url);
        }
    }
    render(){
        const menulist=JSON.parse(storage.getItem("menulist"));
        var menuJSX=menulist.map(function(item) {
            return <Menu.Item key={item.url}><Icon type={item.icon} />{item.name}</Menu.Item>
        }, this);
        const el=(
            <div className="sidebar">
                <Menu
                    onClick={this.handleClick}
                    style={{ width: 200 }}
                    defaultSelectedKeys={['1']}
                    defaultOpenKeys={['sub1']}
                    mode="inline"
                >{menuJSX}</Menu>
            </div>
        );
        return el;
    }
}

export default SiderbarComponent;