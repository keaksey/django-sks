import React, { Component } from 'react'
import { graphql, compose } from 'react-apollo'
import { Field, reduxForm } from 'redux-form'

import { AUTH_TOKEN } from './../../constants'
import { Forms, Button } from './../../components'
import { LOGIN_MUTATION } from './mutation'

class Login extends Component {
    constructor(props) {
        super(props);
        
        this.handleSubmit = this.handleSubmit.bind(this);
    }
    
    async handleSubmit(field) {
        const result = await this.props.tokenCreate({
            variables: {...field},
        });
        
        const { errors, token } = result.data.tokenCreate;
        
        if ( errors ) {
            console.log('errors ', errors);
        }else {
            localStorage.setItem(AUTH_TOKEN, token);
        }
        
    }
    
    render() {
        
        const { handleSubmit } = this.props;
        
        return (
            <div className="container py-5">
                <div className="row">
                    <div className="col-md-12">
                        <h2 className="text-center text-white mb-4">Bootstrap 4 Login Form</h2>
                        <div className="row">
                            <div className="col-md-6 mx-auto">
                                <div className="card rounded-0">
                                    <div className="card-header">
                                        <h3 className="mb-0">Login</h3>
                                    </div>
                                    <div className="card-body">
                                        <form className="form" role="form" autoComplete="off" 
                                            noValidate onSubmit={handleSubmit(this.handleSubmit)}
                                        >
                                            <div className="form-group">
                                                <label htmlFor="username">Username</label>
                                                <Field 
                                                    component={Forms.renderField}
                                                    name="username"
                                                    type="text"
                                                    className="form-control form-control-lg rounded-0"
                                                />
                                                <div className="invalid-feedback">Oops, you missed this one.</div>
                                            </div>
                                            <div className="form-group">
                                                <label>Password</label>
                                                <Field 
                                                    component={Forms.renderField}
                                                    name="password"
                                                    type="password"
                                                    className="form-control form-control-lg rounded-0"
                                                />
                                                <div className="invalid-feedback">Enter your password too!</div>
                                            </div>
                                            <div>
                                                <label className="custom-control custom-checkbox">
                                                  <input type="checkbox" className="custom-control-input" />
                                                  <span className="custom-control-indicator"></span>
                                                  <span className="custom-control-description small text-dark">Remember me on this computer</span>
                                                </label>
                                            </div>
                                            <Button type="submit" className="btn btn-success btn-lg float-right" id="btnLogin">Login</Button>
                                        </form>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        )
    }
}

Login = reduxForm({
    form: 'LoginForm'
})(Login)

export default compose(
  //graphql(SIGNUP_MUTATION, { name: 'signupMutation' }),
  graphql(LOGIN_MUTATION, { name: 'tokenCreate' }),
)(Login)

