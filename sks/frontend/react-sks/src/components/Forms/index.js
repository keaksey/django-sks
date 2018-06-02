import React from 'react'
import PropTypes from 'prop-types'

const propsTypes = {
    input: PropTypes.object
}

export const renderField = (props: propsTypes) =>{
    let { 
        input, 
        type, 
        label, 
        placeholder, 
        multiline, 
        prefix, 
        helpText, 
        labelAction,
        min,
        options,
        connectedRight,
        readOnly,
        meta: { touched, error },
        className
    } = props;
    
    return (
        <div className={`${'form-group '} ${type !== 'hidden' ? '': 'd-none'}`}>
            <input {...input} className={className || ''} type={type} />
        </div>
    )
}