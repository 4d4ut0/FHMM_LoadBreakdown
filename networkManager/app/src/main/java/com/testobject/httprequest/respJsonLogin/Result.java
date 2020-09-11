package com.testobject.httprequest.respJsonLogin;

import java.util.ArrayList;
import java.io.Serializable;

public class Result implements Serializable{
    private int idUsuario;
    private String nome;
    private String email;
    private String senha;
    private Integer porcentagem;
    private Boolean ativo;
    private Integer totalEnergiaGerada;
    private Integer energiaDisponivel;
    private String cpf;
    private Perfil perfil;
    private ArrayList<Perfil> perfis;
    private String endereco;

    public int getIdUsuario() {
        return idUsuario;
    }

    public void setIdUsuario(int idUsuario) {
        this.idUsuario = idUsuario;
    }

    public String getNome() {
        return nome;
    }

    public void setNome(String nome) {
        this.nome = nome;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getSenha() {
        return senha;
    }

    public void setSenha(String senha) {
        this.senha = senha;
    }


    public Integer getPorcentagem() {
        return porcentagem;
    }

    public void setPorcentagem(Integer porcentagem) {
        this.porcentagem = porcentagem;
    }

    public Boolean getAtivo() {
        return ativo;
    }

    public void setAtivo(Boolean ativo) {
        this.ativo = ativo;
    }

    public Integer getTotalEnergiaGerada() {
        return totalEnergiaGerada;
    }

    public void setTotalEnergiaGerada(Integer totalEnergiaGerada) {
        this.totalEnergiaGerada = totalEnergiaGerada;
    }

    public Integer getEnergiaDisponivel() {
        return energiaDisponivel;
    }

    public void setEnergiaDisponivel(Integer energiaDisponivel) {
        this.energiaDisponivel = energiaDisponivel;
    }

    public String getCpf() {
        return cpf;
    }

    public void setCpf(String cpf) {
        this.cpf = cpf;
    }

    public Perfil getPerfil() {
        return perfil;
    }

    public void setPerfil(Perfil perfil) {
        this.perfil = perfil;
    }

    public ArrayList<Perfil> getPerfis() {
        return perfis;
    }

    public void setPerfis(ArrayList<Perfil> perfis) {
        this.perfis = perfis;
    }

    public String getEndereco() {
        return endereco;
    }

    public void setEndereco(String endereco) {
        this.endereco = endereco;
    }
}
