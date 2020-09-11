package com.testobject.httprequest;


import android.content.Intent;
import android.os.Bundle;
import androidx.annotation.NonNull;
import com.google.android.material.bottomnavigation.BottomNavigationView;

import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentTransaction;
import androidx.appcompat.app.AppCompatActivity;
import android.view.MenuItem;
import com.testobject.httprequest.Fragments.AnualFragment;
import com.testobject.httprequest.Fragments.DiarioFragment;
import com.testobject.httprequest.Fragments.MensalFragment;


public class UserConsumoActivity extends AppCompatActivity {

    private String userName;
    private String userId;
    private String estacaoId;
    private String estacaoName;
    private BottomNavigationView bottomNavigation;
    private Bundle bundle;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_user_consumo);
        bottomNavigation = findViewById(R.id.bottom_navigation);
        bottomNavigation.setOnNavigationItemSelectedListener(navigationItemSelectedListener);


        Intent intent = getIntent();
        bundle = intent.getExtras();
        if (bundle != null){
            userName = getIntent().getStringExtra("userName");
            userId = getIntent().getStringExtra("userId");
            estacaoId = getIntent().getStringExtra("estacaoId");
            estacaoName = getIntent().getStringExtra("estacaoName");
        }

        openFragment(DiarioFragment.newInstance(userName, userId, estacaoId, estacaoName));
    }

    public void openFragment(Fragment fragment) {
        FragmentTransaction transaction = getSupportFragmentManager().beginTransaction();
        transaction.replace(R.id.container, fragment);
        transaction.addToBackStack(null);
        transaction.commit();
    }

    BottomNavigationView.OnNavigationItemSelectedListener navigationItemSelectedListener =
            new BottomNavigationView.OnNavigationItemSelectedListener() {
                @Override public boolean onNavigationItemSelected(@NonNull MenuItem item) {
                    switch (item.getItemId()) {
                        case R.id.navigation_diario:
                            openFragment(DiarioFragment.newInstance(userName, userId, estacaoId, estacaoName));
                            return true;
                        case R.id.navigation_mensal:
                            openFragment(MensalFragment.newInstance(userName, userId, estacaoId, estacaoName));
                            return true;
                        case R.id.navigation_anual:
                            openFragment(AnualFragment.newInstance(userName, userId, estacaoId, estacaoName));
                            return true;
                    }
                    return false;
                }
            };

}
