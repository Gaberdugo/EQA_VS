import { useEffect } from "react";
import { connect } from "react-redux";
import { check_authenticates, load_user, refresh } from "redux/actions/login/auth";

function Layout({
    children,
    check_authenticates,
    refresh,
    load_user, 
    user_loading,
    isAuthenticade,
    user,
}){

    useEffect(()=>{
        isAuthenticade ? <></>:
        <>
            {refresh()}
            {check_authenticates()}
            {load_user()}
        </>
    },[])

    return(
        <div>
            {children}
        </div>
    )
}

const mapStateToProps = state => ({
    user_loading: state.auth.user_loading,
    isAuthenticade: state.auth.isAuthenticade,
    user: state.auth.user,
})

export default connect(mapStateToProps,{
    check_authenticates,
    refresh,
    load_user,
}) (Layout)