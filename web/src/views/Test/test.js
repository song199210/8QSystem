// 改造前，注意 _addItem 实现
import React from 'react'
import PureRenderMixin from 'react-addons-pure-render-mixin'
 
class App extends React.Component {
　　constructor(props){
        super(props)
　　　　this.state = {
　　　　　　items: {name:123123123}
　　　　}
        this._addItem=this._addItem.bind(this)
　　　　// 添加 PureRenderMixin 的语句
　　　　this.shouldComponentUpdate = PureRenderMixin.shouldComponentUpdate
　　　　// 通过 React.createClass 新建的组件可以直接在其 mixins: 属性中添加 PureRenderMixin 即可 
　　　　mixins: [PureRenderMixin]
　　}  
    shouldComponentUpdate(){
        
    }
　　render() {
        let chkGroup=null;
        for(var i=0;i<10000;i++){
            chkGroup
        }
　　　　return (<div>
　　　　　　　　　　<button onClick={ this._addItem }> 添加随机数据 </button>
　　　　　　　　　　<ul>
　　　　　　　　　　　　<li> {this.state.items.name} </li>
　　　　　　　　　　</ul>
　　　　　　　　</div>)
　　}
　　_addItem() {
　　　　// 直接对 items 进行 push 操作，
　　　　this.setState({
　　　　　　items: {name:Math.ceil(Math.random()*1000)}
　　　　})
　　}
}
export default App;