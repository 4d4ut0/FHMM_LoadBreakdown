package com.testobject.httprequest.respDeviceCadastro;

public class DeviceCadastro {
    private String idEstacao;
    private String tipo;
    private String apelido;

    public String getIdEstacao() {
        return idEstacao;
    }

    public void setIdEstacao(String idEstacao) {
        this.idEstacao = idEstacao;
    }

    public String getTipo() {
        return tipo;
    }

    public void setTipo(String tipo) {
        this.tipo = tipo;
    }

    public String name(){
        if(this.tipo.equals("outro")) return this.apelido;
        return this.tipo;
    }

    public String getApelido() {
        return apelido;
    }

    public void setApelido(String apelido) {
        this.apelido = apelido;
    }
}
