package com.testobject.httprequest.Adapters;

import android.content.Context;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.testobject.httprequest.R;
import com.testobject.httprequest.respDevice.Device;
import com.testobject.httprequest.respHorimetro.Horimetro;

import java.util.List;

public class HorimetrosAdapter extends RecyclerView.Adapter<HorimetrosAdapter.HorimetroViewHolder> {
    @NonNull

    private Context mCtx;
    private List<Horimetro> horimetrosList;

    public HorimetrosAdapter(Context mCtx, List<Horimetro> horimetrosList) {
        this.mCtx = mCtx;
        this.horimetrosList = horimetrosList;
    }

    @Override
    public HorimetroViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        LayoutInflater inflater = LayoutInflater.from(mCtx);
        View view = inflater.inflate(R.layout.layout_horimetros, null);
        return new HorimetroViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull HorimetroViewHolder holder, int position) {
        Horimetro horimetro = horimetrosList.get(position);


        holder.txt_nome.setText(horimetro.getReferencia());
        holder.txt_mac.setText(horimetro.getIdHardware());
        holder.txt_pontoI.setText(horimetro.getHorarioPontoInicio());
        holder.txt_pontoF.setText(horimetro.getHorarioPontoTermino());

        holder.img_icon.setBackground((horimetro.getOnline())? mCtx.getDrawable(R.drawable.cercleshape_on) :  mCtx.getDrawable(R.drawable.cercleshape_off));

    }

    @Override
    public int getItemCount() {
        return horimetrosList.size();
    }

    public static class HorimetroViewHolder extends RecyclerView.ViewHolder{
        TextView txt_nome, txt_mac, txt_pontoI, txt_pontoF;
        ImageView img_icon;

        public HorimetroViewHolder(@NonNull View itemView) {
            super(itemView);

            txt_nome = itemView.findViewById(R.id.txt_nome);
            txt_mac = itemView.findViewById(R.id.txt_mac);
            txt_pontoI = itemView.findViewById(R.id.txt_pontoI);
            txt_pontoF = itemView.findViewById(R.id.txt_pontoF);
            img_icon = itemView.findViewById(R.id.img_icon);
        }
    }
}