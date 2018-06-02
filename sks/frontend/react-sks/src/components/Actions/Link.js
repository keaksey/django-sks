import React from 'react'
import { Link as RouterLink } from 'react-router-dom'

const Link = (props) => {
    
    return (
        <RouterLink to={props.to} 
            className={`${props.type === 'button' ? 'btn': ''} ${props.className || ''}`}
        >
            {props.children}
        </RouterLink>
    )
}

export default Link

