package com.testobject.httprequest.respJsonInstaller;

import android.util.Log;

import com.testobject.httprequest.respJsonLogin.Result;

import java.util.ArrayList;
import java.util.List;

public class respJsonInstaller {
    private ArrayList<ResultInstaller> result;
    private String message;
    private String objetoGenerico;
    private Integer qtdTotal;

    public List<String> getAllNameUser(){
        List<String> allName = new ArrayList<>();

        for(int i = 0; i < result.size(); i++) {
            allName.add(result.get(i).getNome());
        }

        return allName;
    }

    public List<Integer> getAllIdUser(){
        List<Integer> allId = new ArrayList<>();

        for(int i = 0; i < result.size(); i++)
            allId.add(result.get(i).getIdUsuario());

        return allId;
    }

    public List<Boolean> getAllStatusUser(){
        List<Boolean> allStatus = new ArrayList<>();

        for(int i = 0; i < result.size(); i++)
            allStatus.add(result.get(i).getAtivo());

        return allStatus;
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

    public Integer getQtdTotal() {
        return qtdTotal;
    }

    public void setQtdTotal(Integer qtdTotal) {
        this.qtdTotal = qtdTotal;
    }

    public ArrayList<ResultInstaller> getResult() {
        return result;
    }

    public void setResult(ArrayList<ResultInstaller> result) {
        this.result = result;
    }
}
