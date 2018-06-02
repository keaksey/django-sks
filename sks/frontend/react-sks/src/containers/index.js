// @flow
import React, { Component } from 'react'

import {
    Navbar
} from './../components'

import Routes from './Routes'

class App extends Component<{}> {
    
    render() {
        return (
            <React.Fragment>
                <header className="app-header">
                    <Navbar />
                </header>
                <div className="container-fluid">
                    <Routes />
                </div>
            </React.Fragment>
        );
    }
}

export default App

