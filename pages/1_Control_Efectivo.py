with col_chart2:
                    st.markdown("#### 🏆 Top 10 Puntos de Venta (Mayor Recaudo)")
                    df_top = df_ext_gen[df_ext_gen['PDV_SAP'] != ''].groupby('PDV_SAP').agg(
                        Recaudo=('VALOR_LIMPIO', 'sum')
                    ).reset_index().nlargest(10, 'Recaudo')
                    
                    if len(df_top) > 0:
                        # Creamos una columna para diferenciar el color de la barra #1 vs las demás
                        df_top['EsTop1'] = df_top['Recaudo'] == df_top['Recaudo'].max()
                        
                        # Capa de barras horizontales
                        bars = alt.Chart(df_top).mark_bar(
                            cornerRadiusTopRight=6, 
                            cornerRadiusBottomRight=6
                        ).encode(
                            x=alt.X('Recaudo:Q', title=None, axis=alt.Axis(format="$,s", grid=False)),
                            y=alt.Y('PDV_SAP:N', sort='-x', title=None, axis=alt.Axis(labelLimit=220)),
                            color=alt.Color(
                                'EsTop1:N',
                                scale=alt.Scale(domain=[True, False], range=['#6b1d3f', '#E91E63']),
                                legend=None
                            ),
                            tooltip=['PDV_SAP', alt.Tooltip('Recaudo', format="$,.2f", title="Recaudo Total")]
                        )
                        
                        # Capa de texto con el valor exacto a la derecha de cada barra
                        text = alt.Chart(df_top).mark_text(
                            align='left',
                            baseline='middle',
                            dx=6,  # Desplazamiento a la derecha de la barra
                            fontSize=11,
                            fontWeight='bold',
                            color='#4B5563'
                        ).encode(
                            x=alt.X('Recaudo:Q'),
                            y=alt.Y('PDV_SAP:N', sort='-x'),
                            text=alt.Text('Recaudo:Q', format="$,.0f")
                        )
                        
                        # Combinamos ambas capas en un solo gráfico limpio
                        chart_top10 = (bars + text).properties(height=320).configure_view(strokeWidth=0)
                        
                        st.altair_chart(chart_top10, use_container_width=True)
                    else:
                        st.info("No hay suficientes datos de PDV SAP identificados para mostrar el Top 10.")
