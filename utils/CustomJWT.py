def jwt_response_payload_handler(token, user=None, request=None):
    """
    自定义jwt认证成功返回数据
    """
    return {
        'token': token,
        'id': user.id,
        'username': user.username,
        'mobile': user.mobile,
        'avatar': user.avatar
<<<<<<< Updated upstream
<<<<<<< HEAD
    }
=======
    }
>>>>>>> sanbai
=======
    }
>>>>>>> Stashed changes
