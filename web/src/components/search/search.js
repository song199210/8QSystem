import React from "react";
import { Input,Icon } from 'antd';
import "./search.scss";

const Search = Input.Search;

export default (props)=>{
    const title=props.title;
    return (
        <div className="search_box">
            <span>{title}</span>
            <Search
            placeholder="请输入关键字进行搜索"
            onSearch={(value)=>props.handleFuns(value)}
            enterButton
            style={{ width: 260 }}
            />
        </div>
    )
}