package com.testobject.httprequest.respJsonLogin;

import java.io.Serializable;

public class Perfil implements Serializable{
    private Integer idPerfil;
    private String nome;
    private String descricao;
    private Integer usuarios;

    public Integer getIdPerfil() {
        return idPerfil;
    }

    public void setIdPerfil(Integer idPerfil) {
        this.idPerfil = idPerfil;
    }

    public String getNome() {
        return nome;
    }

    public void setNome(String nome) {
        this.nome = nome;
    }

    public String getDescricao() {
        return descricao;
    }

    public void setDescricao(String descricao) {
        this.descricao = descricao;
    }

    public Integer getUsuarios() {
        return usuarios;
    }

    public void setUsuarios(Integer usuarios) {
        this.usuarios = usuarios;
    }
}
