import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import {Store} from "./redux/index";
import registerServiceWorker from './registerServiceWorker';

const renderApp=()=>{
    return ReactDOM.render(<App />, document.getElementById('root'));
};

Store.subscribe(renderApp);
renderApp();
registerServiceWorker();
