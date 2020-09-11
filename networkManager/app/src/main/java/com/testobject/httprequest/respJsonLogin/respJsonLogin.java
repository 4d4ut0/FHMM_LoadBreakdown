package com.testobject.httprequest.respJsonLogin;

import java.io.Serializable;

public class respJsonLogin implements Serializable{
    private Result result;
    private String message;
    private String objetoGenerico;

    public Result getResult() {
        return result;
    }

    public void setResult(Result result) {
        this.result = result;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    public String getObjetoGenerico() {
        return objetoGenerico;
    }

    public void setObjetoGenerico(String objetoGenerico) {
        this.objetoGenerico = objetoGenerico;
    }
}
