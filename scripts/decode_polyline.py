def decode_polyline(polyline):
    points = []
    index = lat = lng = z = 0

    while index < len(polyline):
        result = 1
        shift = 0
        while True:
            b = ord(polyline[index]) - 63 - 1
            index += 1
            result += b << shift
            shift += 5
            if b < 0x1F:
                break
        lat += (~result >> 1) if (result & 1) != 0 else (result >> 1)

        result = 1
        shift = 0
        while True:
            b = ord(polyline[index]) - 63 - 1
            index += 1
            result += b << shift
            shift += 5
            if b < 0x1F:
                break
        lng += ~(result >> 1) if (result & 1) != 0 else (result >> 1)
        points.append([round(lng * 1e-6, 6), round(lat * 1e-6, 6)])
    return points 
    


# print(decode_polyline("udfbzAw_vqa@bF~BdIvE|BlAFwRPq^Tuh@nAixCDuPVwo@BiMHqn@Jkq@@eH`BylAfAwP|HabAlC}]pM{dBlEcm@lAkT^wMV}MLe_@EsJOwHq@mTeA_S_A{N{Deb@vCsBrCqHgIc`@wA{GcEyRsJWkG_TqI_VsCqIaAaCkGqO{BgE{MaVsLePwMwPwMwNiQcPoJwFeLmGcLoFuMeFi^uMadB_o@an@o\\aVkMyPaJ{f@}X_P}K{BoAma@oWsV}Pui@aa@ib@}\\q]kXko@cf@wh@ca@uU_QwJ{GoNwI}Q_LaaAmk@{NqI}OwIkOkIgQsIuh@uVg[cOo\\uO}y@_^urBebAyMuGsQkKkTwMcSyMeSoMaOsJ}RuN{QeNsX_TiX_T_n@{h@cl@ui@mh@}h@cS_TyR}SiSeU{@cAyGqH}GsIgNoQoWs]cSgXaIqKsHgKqIwLwIcM}HgLgHuKoF}IuFsI_LaR_KcPcK_Q}Uma@u[ui@i[{i@mw@utAepBsjDs_@_r@oJ{OuE}H{NyVgMkSs]qj@}HoKkQiUaSkVu[i^o^c_@i[wXiNwKsOyKyJeHeNiJcZaQmXsN}KwFiM}FyNsGyPsGcPwFeRwFmO}EmQqEuPkD_HoA}JiBgNgBmOcBea@kD{_@eBmOa@kQ_@eKC{KJoLRs[nA_Q`AsQpBkTzBsUxCo\\jGaN~CcMpC{NtD_NnDaNhE}LbFoSrHwQ~Hic@nUkoAbl@mjB~|@qkBv|@arE`yBkNhH{dPzaIub@|ScqAjo@of@xV{f@pUyV|J{UpJcWzI{JdDm]pJiP~DqOpDwPhD_PfD}PvCuOhCuQ`CcN|AoNlAk_@pCsV|@uTd@}U^{VJsZW{Wu@ym@yBebBgHya@yAgn@uAyPi@qQ_A{q@yD_HYu{@oDqq@gD{y@iC_nBgJoH[qnAeFmW{@_d@k@sh@]aq@Ae~@?qFGeHWuEe@aE_AkCw@wH{CsB{@}BcAuKsF}\\uPgUcLgKgF}G}CgCcAaC_AyDkA{FyA{GsA}NoCsJcBaV{EaMoC_JuByJwCsGwB}GuC_JcEeHsDkGiDoHqE{LiJgI_H}TaT{a@ed@qHgIkFwGyDqF}E_ImDyGmDcHqCoGeGgN{IoTwEuLgSmo@eH}V_EcQiF}W}D}UmC_RuAqM_AkKgB}T_BoUkEst@mAgQuA}UyAkT{@wJyA}MiAiJcA{GaAmFcA_FcA{DsAcEuBuE_EsGeAqAkBwBiCeCcDsC{@s@yG}E}ZgSyYwR_y@ck@w_@eXuIgGoHiFkb@eZ_`@}VeTgN}FyD{k@i_@gZkSwMoK{_@{]eU}SmKcKuGyFyAuA{DqCyCqBcE_CyEmBuC_AwC}@}Cm@wCe@kD_@sCOcHMuNQ_IO{L}@kCa@yCm@yCu@mFaBiJqDuW_KeGwBqMwEaEyAoO_GcRkHoMqGeEsBaRwJ}MiHqPiJcLaH}MqHuEgC_^sSgFoCoOoIgVuMs\\wR}b@qUyEmC}WmOs_BmaAwCmBsD}Bua@yWaN}IqOuKqEoC_b@sWgBeAgT}MoCeBa@Uca@wTeHiDqJuE{IiDyNmEqIeCuKeCcJuAkKkA{DQ{CSuKO_JFyJXaKt@kJz@o[nCoILiJV}OLeQKgOSkJ[sHe@yDSwF{@{Dm@uFsA_IyBqDgAaE}AeEgBeFqCiOkKcq@wf@sIsH{C{C_DoDaCmCiCuD_CuDkBeDgBoDaCmEaCkFoDaH}GiMoEuIiE}G{CaEsCiD{DmEmFmG}GaG_IsF_GeDwDmB}D_BeGuBuD_AaF_AmDe@mOoAsm@yCe|@wEmp@gDy]gBsAGmjA{F_q@iDkY}AaW}BaOoAcOwBc@Gu_@mGwMcCyCk@}QsEqTiG_VeIc^_P_SqJkWaM{YaRkPiKcUyOoVkP{TyQ_JkIiHwH}KiM_MoN}K{M_K_NgN_S{NyTuCgEcNeWiPqZkOsXsCoFkd@y{@cQk\\}C}F}BaE}`BqvCqFyJyHgNsO_ZiFsIgGcJcG}IqHmJgG_HwFuEqJoIcHkFmKaH}JcHgIgEiE}BuHwBmIoCoKwCmLqBmMwAiKs@gKOoJWkNRyVjAaFp@wFbAqFfAoCh@wBh@cGrBgFtBoL`FuKlF}kAjo@}p@l^km@j[of@bZiGvDqFpD_C|AkBtAeDjC_EjDqDlDsDxDiDvDsDlEcDlEyIhM}n@x~@c`@rk@iBfCoTxZ{JhNeB`C_BxBuIhLcO|PsHlHyIfHuPlLcGfCoHrD}L~DaF|AyFtAqFjAoG`A{D^cCTkLf@mgA~FmdAbH_AF_~BfJga@Go`@SkLGs\\fAwU|A}KlAmJpA{IjA}HvAwPtD{g@dMiNxDkLtDuR`IcWjKcHtC}NtI{WhOaf@|Yqu@fi@mM~JkR~N{DvCcAz@sqAz_Au_BllA_dAds@em@d]gpAtl@e{BtaAikBl|@u_Fj}BojChoAasBbbAiQpI_eCdkAs_Brv@sMhGwHxDif@zUekDlbBsQvIoxCjwAqg@dUko@nYyc@nSmu@|\\oj@xXq}@rc@we@`UqDfByc@jSseAbf@w]~OsLbGiEvBm`@zR_XzMg|Alv@w^jQwS~JcH|CkHlDw_@vQyUpL}MvGaWbMml@vYky@t^gQ|IyFpC_Bv@qJzEiXdM_n@|[iGvCqY|Ls\\dPiG`DeM~FmS~HgItCeKbAmHCa|@b@i`Bp@qJyEuF}BS{@Yw@_@o@c@i@g@_@i@Uk@Mk@Ak@Fk@Ng@Ze@`@_@j@]p@Wv@O|@K~@C~@mArCwDbFuDbJ}KtMsRfUwAvA}CjEaDxEmH~JcCrDsDlF{I|LsLhRoU|^_Zzd@oLbQqGpJkObVa[x_@u@|@yFdEgDbCiE~CkRpNeGzEqJ|GePxL}JrHwEfEeDiK}Pqe@eMoa@aFeO_FcKiBiBiw@ux@}\\q\\uHuH_NkOam@wj@qEmD}B{AaGqBep@d{AaG`HyMiQu@mGZyAj]sr@`Po^zItCpMvEu\\tv@",False))
