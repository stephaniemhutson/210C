/**************************************************************
ECON 210C: Problem Set 1
Stephanie Hutson
(Thank you John Juneau!)
**************************************************************/

/* 0) Preamble ***********************************************
************************************************************/{
	clear
	cd "/Users/stephaniehutson/Desktop/Economics/210C/PS2"
	* Packages 
	// 	ssc install blindschemes, replace
	// 	ssc install GRSTYLE, replace
	// 	ssc install freduse, replace
	
	* Import data method
	global withfreduse = 0
	
	*Establish color scheme
	global bgcolor "211 216 221"
	global fgcolor "15 60 15"
		/* Decomp Colors */
		global color1 "255 87 51"
		global color2 "0 63 125"
		global color3 "102 38 93"
		
	* Establish some graphing setting
	graph drop _all
	set scheme plotplainblind // Biscoff
	grstyle init
	// Legend settings
	grstyle set legend 6, nobox
	// General plot 
	grstyle color background "${bgcolor}"
	grstyle color major_grid "${fgcolor}"
	grstyle set color "${fgcolor}": axisline major_grid // set axis and grid line color
	grstyle linewidth major_grid thin
	grstyle yesno draw_major_hgrid yes
	grstyle yesno grid_draw_min yes
	grstyle yesno grid_draw_max yes
	grstyle anglestyle vertical_tick horizontal
}	

/* 1) Load data from FRED
************************************************************/{
	/* a. Get data from FRED  */ {
		clear
		local tsvar "FEDFUNDS UNRATE GDPDEF USRECM"
		if ${withfreduse} == 1 {
			freduse `tsvar', clear 
			
		}
		if ${withfreduse} == 0 {
			foreach v of local tsvar {
				import delimited using "data/`v'.csv", clear case(preserve)
				rename DATE date
				tempfile `v'_dta
				save ``v'_dta', replace
			}
			use `FEDFUNDS_dta', clear
			keep date
			foreach v of local tsvar {
				joinby date using ``v'_dta', unm(b)
				drop _merge
			}
		}
	}
	
	/* b. Clean data */{
		if ${withfreduse} == 0 {
			gen daten = date(date, "YMD")
			format daten %td
		}
		drop if yofd(daten) < 1960  | yofd(daten) > 2023 // data is per quarter in 1947 but per month after 
		gen INFL = 100*(GDPDEF - GDPDEF[_n-12])/GDPDEF[_n-12] //year to year inflation
			la var INFL "Inflation Rate"
			la var FEDFUNDS "Federal Funds Rate"
			la var UNRATE "Unemployment Rate"
			la var daten Date // re=label date 
		local tsvar "FEDFUNDS UNRATE INFL" // Reset local varlist to include created inflation var
	}
	
	/* c. Format recession bars */{
		egen temp1 = rowmax(`tsvar')
		sum temp1
		local max = ceil(r(max)/5)*5
		generate recession = `max' if USREC == 1
		drop temp1
		egen temp1 = rowmin(`tsvar')
		sum temp1
		if r(min) < 0 {
			local min = ceil(abs(r(min))/5)*-5
		}
		if r(min) >= 0 {
			local min = floor(abs(r(min))/5)*5
		}
			replace  recession = `min' if USREC == 0 //
		drop temp1
		la var recession "NBER Recessions"
	}
	
	/* d. Graph the data */ {
	tsset daten
	twoway (area recession daten, color("${fgcolor}") base(`min')) ///
		(tsline FEDFUNDS, lc("${color1}") lp(solid) lw(medthick)) || ///
		(tsline UNRATE, lc("${color2}") lp(dash) lw(medthick)) || ///
		(tsline INFL, lc("${color3}") lp(dot) lw(medthick)) || ///
		, ///
		title("Monthly U.S. Macroeconomic Indicators, 1960-2023", c("${fgcolor}")) ///
		tlabel(, format(%dCY) labc("${fgcolor}")) ttitle("") ///
		yline(0, lstyle(foreground) lcolor("${fgcolor}") lp(dash)) ///
		caption("Source: FRED." "Note: Shaded regions denote recessions.", c("${fgcolor}")) ///
		ytitle("Percent", c("${fgcolor}")) ///
		name(raw_data) ///
		legend(on order(2 3 4) pos(6) bmargin(tiny) r(1))  //bplacement(ne) 
// 	graph export "figures/fig1.pdf", replace
	}
}	

/* 2) Quarterly VAR 
************************************************************/{
	gen dateq = qofd(daten)
	collapse (mean) `tsvar' (max) recession (last) date daten, by(dateq)
	tsset dateq, quarterly
	keep if (yofd(daten) >= 1960) & (yofd(daten) <= 2007)
	var INFL UNRATE FEDFUNDS, lags(1/4)
		irf set var_results, replace
		irf create var_result, step(20) set(var_results) replace
		irf graph irf, impulse(INFL UNRATE FEDFUNDS) response(INFL UNRATE FEDFUNDS) byopts(yrescale) /// INFL UNRATE
			yline(0, lstyle(foreground) lcolor("${fgcolor}") lp(dash)) ///
			name(var_results)
}	

/* 2) Quarterly SVAR 
************************************************************/{
	/* Manual Choleshy Decomp */
	matrix A = (1,0,0 \ .,1,0 \ .,.,1)
	matrix B = (.,0,0 \ 0,.,0 \ 0,0,.)
	svar INFL UNRATE FEDFUNDS, lags(1/4) aeq(A) beq(B)
	irf create mysirf, set(mysirfs) step(20) replace
	irf graph sirf, impulse(INFL UNRATE FEDFUNDS) response(INFL UNRATE FEDFUNDS) ///
			yline(0, lstyle(foreground) lcolor("${fgcolor}") lp(dash)) ///
			name(svar_results_manual)

	var INFL UNRATE FEDFUNDS, lags(1/4)
	irf create myirf, set(myirfs) step(20) replace
	irf graph oirf, impulse(INFL UNRATE FEDFUNDS) response(INFL UNRATE FEDFUNDS) ///
			yline(0, lstyle(foreground) lcolor("${fgcolor}") lp(dash)) ///
			name(svar_results_oirf)
	
}	

/*Romer Shocks*/
/*Merge data*/
// merge 1:1 date dateq using data/RR_monetary_shock_monthly keep(resid)

save vars.dta, replace
use data/RR_monetary_shock_monthly.dta

gen day=dofm(date)
format day %td
gen dateq=qofd(day)
format dateq %tq

drop date
drop day

collapse (mean) resid (mean) resid_romer (mean) resid_full, by(dateq)

merge 1:1 dateq using vars
/* Set values of shocks to zero before 1969 */
replace resid_full = 0 if yofd(daten) <1969

save romer.dta, replace

// tsset date
// var INFL UNRATE FEDFUNDS, lags(1/8)  exog(L(0/12).resid_full)
// irf create myrirf, step(12) replace
// irf graph dm, impulse(resid_full) irf(myrirf)
// graph export question2b_plot.pdf, replace

/* Construct irf from estimation equation */{
	tsset dateq
	var INFL UNRATE FEDFUNDS, lags(1/8) exog(L(0/12).resid_full)
		irf set RR_var_results, replace
		irf create var_result, step(12) set(RR_var_results) replace
		irf graph irf, impulse(INFL UNRATE FEDFUNDS) response(INFL UNRATE FEDFUNDS) byopts(yrescale) /// INFL UNRATE
			yline(0, lstyle(foreground) lcolor("${fgcolor}") lp(dash)) ///
			name(RR_var_results)
}

/*Constring SVAR ordered RR pi u R */{
	matrix A = (1,0,0,0 \ .,1,0,0 \ .,.,1,0 \ .,.,.,1)
	matrix B = (.,0,0,0 \ 0,.,0,0 \ 0,0,.,0 \0,0,0,.)
	svar resid_full INFL UNRATE FEDFUNDS, lags(1/4) aeq(A) beq(B)
	irf create myRRsirf, set(myRRsirfs) step(20) replace
	irf graph sirf, impulse(resid_full INFL UNRATE FEDFUNDS) response(resid_full INFL UNRATE FEDFUNDS) ///
			yline(0, lstyle(foreground) lcolor("${fgcolor}") lp(dash)) ///
			name(svar_rr_results_manual)

	var resid_full INFL UNRATE FEDFUNDS, lags(1/4)
	irf create myrrirf, set(myrrirfs) step(20) replace
	irf graph oirf, impulse(resid_full INFL UNRATE FEDFUNDS) response(resid_full INFL UNRATE FEDFUNDS) ///
			yline(0, lstyle(foreground) lcolor("${fgcolor}") lp(dash)) ///
			name(svar_rr_results_oirf)
}

