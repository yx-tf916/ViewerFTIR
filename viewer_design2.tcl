#############################################################################
# Generated by PAGE version 8.0
#  in conjunction with Tcl version 8.6
#  Feb 24, 2025 11:59:06 AM PST  platform: Windows NT
set vTcl(timestamp) ""
if {![info exists vTcl(borrow)]} {
    ::vTcl::MessageBox -title Error -message  "You must open project files from within PAGE."
    exit}


set vTcl(actual_gui_font_dft_desc)  TkDefaultFont
set vTcl(actual_gui_font_dft_name)  TkDefaultFont
set vTcl(actual_gui_font_text_desc)  TkTextFont
set vTcl(actual_gui_font_text_name)  TkTextFont
set vTcl(actual_gui_font_fixed_desc)  TkFixedFont
set vTcl(actual_gui_font_fixed_name)  TkFixedFont
set vTcl(actual_gui_font_menu_desc)  TkMenuFont
set vTcl(actual_gui_font_menu_name)  TkMenuFont
set vTcl(actual_gui_font_tooltip_desc)  TkDefaultFont
set vTcl(actual_gui_font_tooltip_name)  TkDefaultFont
set vTcl(actual_gui_font_treeview_desc)  TkDefaultFont
set vTcl(actual_gui_font_treeview_name)  TkDefaultFont
########################################### 
set vTcl(actual_gui_bg) #d9d9d9
set vTcl(actual_gui_fg) #000000
set vTcl(actual_gui_analog) #ececec
set vTcl(actual_gui_menu_analog) #ececec
set vTcl(actual_gui_menu_bg) #d9d9d9
set vTcl(actual_gui_menu_fg) #000000
set vTcl(complement_color) gray40
set vTcl(analog_color_p) #c3c3c3
set vTcl(analog_color_m) beige
set vTcl(tabfg1) black
set vTcl(tabfg2) white
set vTcl(actual_gui_menu_active_bg)  #ececec
set vTcl(actual_gui_menu_active_fg)  #000000
########################################### 
set vTcl(pr,autoalias) 1
set vTcl(pr,relative_placement) 1
set vTcl(mode) Relative
set vTcl(project_theme) default



proc vTclWindow.top1 {base} {
    global vTcl
    if {$base == ""} {
        set base .top1
    }
    if {[winfo exists $base]} {
        wm deiconify $base; return
    }
    set top $base
    set target $base
    ###################
    # CREATING WIDGETS
    ###################
    vTcl::widgets::core::toplevel::createCmd $top -class Toplevel \
        -background #d9d9d9 -highlightbackground #d9d9d9 \
        -highlightcolor #000000 
    wm focusmodel $top passive
    wm geometry $top 1104x740+2248+159
    update
    # set in toplevel.wgt.
    global vTcl
    global img_list
    set vTcl(save,dflt,origin) 0
    wm maxsize $top 3844 1061
    wm minsize $top 120 1
    wm overrideredirect $top 0
    wm resizable $top 1 1
    wm deiconify $top
    set toptitle "Toplevel 0"
    wm title $top $toptitle
    namespace eval ::widgets::${top}::ClassOption {}
    set ::widgets::${top}::ClassOption(-toptitle) $toptitle
    vTcl:DefineAlias "$top" "Toplevel1" vTcl:Toplevel:WidgetProc "" 1
    set vTcl(real_top) {}
    button "$top.but51" \
        -activebackground #d9d9d9 -activeforeground black -background #d9d9d9 \
        -disabledforeground #a3a3a3 -font "-family {Segoe UI} -size 9" \
        -foreground #000000 -highlightbackground #d9d9d9 \
        -highlightcolor #000000 -text "Unset As Background" 
    vTcl:DefineAlias "$top.but51" "Button4" vTcl:WidgetProc "Toplevel1" 1
    button "$top.but55" \
        -activebackground #d9d9d9 -activeforeground black -background #d9d9d9 \
        -disabledforeground #a3a3a3 -font "-family {Segoe UI} -size 9" \
        -foreground #000000 -highlightbackground #d9d9d9 \
        -highlightcolor #000000 -text "Unset As Primary" 
    vTcl:DefineAlias "$top.but55" "Button4_1" vTcl:WidgetProc "Toplevel1" 1
    button "$top.but50" \
        -activebackground #d9d9d9 -activeforeground black -background #d9d9d9 \
        -disabledforeground #a3a3a3 -font "-family {Segoe UI} -size 9" \
        -foreground #000000 -highlightbackground #d9d9d9 \
        -highlightcolor #000000 -text "Set As Background" 
    vTcl:DefineAlias "$top.but50" "Button3" vTcl:WidgetProc "Toplevel1" 1
    button "$top.but54" \
        -activebackground #d9d9d9 -activeforeground black -background #d9d9d9 \
        -disabledforeground #a3a3a3 -font "-family {Segoe UI} -size 9" \
        -foreground #000000 -highlightbackground #d9d9d9 \
        -highlightcolor #000000 -text "Set As Primary" 
    vTcl:DefineAlias "$top.but54" "Button3_1" vTcl:WidgetProc "Toplevel1" 1
    button "$top.but53" \
        -activebackground #d9d9d9 -activeforeground black -background #d9d9d9 \
        -disabledforeground #a3a3a3 -font "-family {Segoe UI} -size 9" \
        -foreground #000000 -highlightbackground #d9d9d9 \
        -highlightcolor #000000 -text "Clear" 
    vTcl:DefineAlias "$top.but53" "Button6" vTcl:WidgetProc "Toplevel1" 1
    button "$top.but62" \
        -activebackground #d9d9d9 -activeforeground black -background #d9d9d9 \
        -disabledforeground #a3a3a3 -font "-family {Segoe UI} -size 9" \
        -foreground #000000 -highlightbackground #d9d9d9 \
        -highlightcolor #000000 -text "Rm Anch." 
    vTcl:DefineAlias "$top.but62" "Button9_1" vTcl:WidgetProc "Toplevel1" 1
    button "$top.but60" \
        -activebackground #d9d9d9 -activeforeground black -background #d9d9d9 \
        -disabledforeground #a3a3a3 -font "-family {Segoe UI} -size 9" \
        -foreground #000000 -highlightbackground #d9d9d9 \
        -highlightcolor #000000 -text "Integrate
Peak" 
    vTcl:DefineAlias "$top.but60" "Button8" vTcl:WidgetProc "Toplevel1" 1
    button "$top.but57" \
        -activebackground #d9d9d9 -activeforeground black -background #d9d9d9 \
        -disabledforeground #a3a3a3 -font "-family {Segoe UI} -size 9" \
        -foreground #000000 -highlightbackground #d9d9d9 \
        -highlightcolor #000000 -text "Cancel Subtr." 
    vTcl:DefineAlias "$top.but57" "Button5_1" vTcl:WidgetProc "Toplevel1" 1
    text "$top.tex66" \
        -background white -font "-family {Segoe UI} -size 9" \
        -foreground black -height 24 -highlightbackground #d9d9d9 \
        -highlightcolor #000000 -insertbackground #000000 \
        -selectbackground #d9d9d9 -selectforeground black -width 67 \
        -wrap word 
    $top.tex66 configure -font "TkTextFont"
    $top.tex66 insert end text
    vTcl:DefineAlias "$top.tex66" "Text1" vTcl:WidgetProc "Toplevel1" 1
    button "$top.but52" \
        -activebackground #d9d9d9 -activeforeground black -background #d9d9d9 \
        -disabledforeground #a3a3a3 -font "-family {Segoe UI} -size 9" \
        -foreground #000000 -highlightbackground #d9d9d9 \
        -highlightcolor #000000 -text "Subtract" 
    vTcl:DefineAlias "$top.but52" "Button5" vTcl:WidgetProc "Toplevel1" 1
    button "$top.but67" \
        -activebackground #d9d9d9 -activeforeground black -background #d9d9d9 \
        -disabledforeground #a3a3a3 -font "-family {Segoe UI} -size 9" \
        -foreground #000000 -highlightbackground #d9d9d9 \
        -highlightcolor #000000 -text "Subtract Group" 
    vTcl:DefineAlias "$top.but67" "Button5_3" vTcl:WidgetProc "Toplevel1" 1
    button "$top.but58" \
        -activebackground #d9d9d9 -activeforeground black -background #d9d9d9 \
        -disabledforeground #a3a3a3 -font "-family {Segoe UI} -size 9" \
        -foreground #000000 -highlightbackground #d9d9d9 \
        -highlightcolor #000000 -text "Save Net" 
    vTcl:DefineAlias "$top.but58" "Button5_2" vTcl:WidgetProc "Toplevel1" 1
    button "$top.but68" \
        -activebackground #d9d9d9 -activeforeground black -background #d9d9d9 \
        -disabledforeground #a3a3a3 -font "-family {Segoe UI} -size 9" \
        -foreground #000000 -highlightbackground #d9d9d9 \
        -highlightcolor #000000 -text "Save Group" 
    vTcl:DefineAlias "$top.but68" "Button5_2_1" vTcl:WidgetProc "Toplevel1" 1
    canvas "$top.can54" \
        -background #d9d9d9 -borderwidth 2 -closeenough 1.0 -height 443 \
        -highlightbackground #d9d9d9 -highlightcolor #000000 \
        -insertbackground #000000 -relief ridge -selectbackground #d9d9d9 \
        -selectforeground black -width 1082 
    vTcl:DefineAlias "$top.can54" "Canvas1" vTcl:WidgetProc "Toplevel1" 1
    button "$top.but47" \
        -activebackground #d9d9d9 -activeforeground black -background #d9d9d9 \
        -disabledforeground #a3a3a3 -font "-family {Segoe UI} -size 9" \
        -foreground #000000 -highlightbackground #d9d9d9 \
        -highlightcolor #000000 -text "Remove" 
    vTcl:DefineAlias "$top.but47" "Button7" vTcl:WidgetProc "Toplevel1" 1
    button "$top.but61" \
        -activebackground #d9d9d9 -activeforeground black -background #d9d9d9 \
        -disabledforeground #a3a3a3 -font "-family {Segoe UI} -size 9" \
        -foreground #000000 -highlightbackground #d9d9d9 \
        -highlightcolor #000000 -text "Add Anch." 
    vTcl:DefineAlias "$top.but61" "Button9" vTcl:WidgetProc "Toplevel1" 1
    button "$top.but48" \
        -activebackground #d9d9d9 -activeforeground black -background #d9d9d9 \
        -disabledforeground #a3a3a3 -font "-family {Segoe UI} -size 9" \
        -foreground #000000 -highlightbackground #d9d9d9 \
        -highlightcolor #000000 -text "Get 
Raw Files
(.csv)" 
    vTcl:DefineAlias "$top.but48" "Button1" vTcl:WidgetProc "Toplevel1" 1
    frame "$top.fra59" \
        -borderwidth 2 -relief groove -background #d9d9d9 -height 155 \
        -highlightbackground #d9d9d9 -highlightcolor #000000 -width 185 
    vTcl:DefineAlias "$top.fra59" "Frame1" vTcl:WidgetProc "Toplevel1" 1
    button "$top.but69" \
        -activebackground #d9d9d9 -activeforeground black -background #d9d9d9 \
        -disabledforeground #a3a3a3 -font "-family {Segoe UI} -size 9" \
        -foreground #000000 -highlightbackground #d9d9d9 \
        -highlightcolor #000000 -text "Multi. Sel." 
    vTcl:DefineAlias "$top.but69" "Button7_1" vTcl:WidgetProc "Toplevel1" 1
    button "$top.but49" \
        -activebackground #d9d9d9 -activeforeground black -background #d9d9d9 \
        -disabledforeground #a3a3a3 -font "-family {Segoe UI} -size 9" \
        -foreground #000000 -highlightbackground #d9d9d9 \
        -highlightcolor #000000 -text "Plot All" 
    vTcl:DefineAlias "$top.but49" "Button2" vTcl:WidgetProc "Toplevel1" 1
    ttk::scale "$top.tSc55" \
        -length 1080 
    vTcl:DefineAlias "$top.tSc55" "TScale1" vTcl:WidgetProc "Toplevel1" 1
    ttk::scale "$top.tSc56" \
        -length 1080 
    vTcl:DefineAlias "$top.tSc56" "TScale2" vTcl:WidgetProc "Toplevel1" 1
    entry "$top.ent71" \
        -background white -disabledforeground #a3a3a3 \
        -font "-family {Courier New} -size 10" -foreground #000000 \
        -highlightbackground #d9d9d9 -highlightcolor #000000 \
        -insertbackground #000000 -selectbackground #d9d9d9 \
        -selectforeground black -width 10 
    vTcl:DefineAlias "$top.ent71" "Entry1_1" vTcl:WidgetProc "Toplevel1" 1
    entry "$top.ent70" \
        -background white -disabledforeground #a3a3a3 \
        -font "-family {Courier New} -size 10" -foreground #000000 \
        -highlightbackground #d9d9d9 -highlightcolor #000000 \
        -insertbackground #000000 -selectbackground #d9d9d9 \
        -selectforeground black -width 10 
    vTcl:DefineAlias "$top.ent70" "Entry1" vTcl:WidgetProc "Toplevel1" 1
    ttk::scale "$top.tSc64" \
        -length 924 
    vTcl:DefineAlias "$top.tSc64" "TScale3" vTcl:WidgetProc "Toplevel1" 1
    listbox "$top.lis47" \
        -background white -disabledforeground #a3a3a3 \
        -font "-family {Courier New} -size 9" -foreground #000000 -height 161 \
        -highlightbackground #d9d9d9 -highlightcolor #000000 \
        -selectbackground #d9d9d9 -selectforeground black -width 379 
    $top.lis47 configure -font "-family {Courier New} -size 9"
    $top.lis47 insert end text
    vTcl:DefineAlias "$top.lis47" "Listbox1" vTcl:WidgetProc "Toplevel1" 1
    entry "$top.ent72" \
        -background white -disabledforeground #a3a3a3 \
        -font "-family {Courier New} -size 10" -foreground #000000 \
        -highlightbackground #d9d9d9 -highlightcolor #000000 \
        -insertbackground #000000 -selectbackground #d9d9d9 \
        -selectforeground black -width 10 
    vTcl:DefineAlias "$top.ent72" "Entry1_2" vTcl:WidgetProc "Toplevel1" 1
    entry "$top.ent73" \
        -background white -disabledforeground #a3a3a3 \
        -font "-family {Courier New} -size 10" -foreground #000000 \
        -highlightbackground #d9d9d9 -highlightcolor #000000 \
        -insertbackground #000000 -selectbackground #d9d9d9 \
        -selectforeground black -width 10 
    vTcl:DefineAlias "$top.ent73" "Entry1_2_1" vTcl:WidgetProc "Toplevel1" 1
    ###################
    # SETTING GEOMETRY
    ###################
    place $top.but51 \
        -in $top -x 0 -relx 0.797 -y 0 -rely 0.068 -width 137 -relwidth 0 \
        -height 26 -relheight 0 -anchor nw -bordermode ignore 
    place $top.but55 \
        -in $top -x 0 -relx 0.67 -y 0 -rely 0.068 -width 137 -relwidth 0 \
        -height 26 -relheight 0 -anchor nw -bordermode ignore 
    place $top.but50 \
        -in $top -x 0 -relx 0.797 -y 0 -rely 0.027 -width 137 -relwidth 0 \
        -height 26 -relheight 0 -anchor nw -bordermode ignore 
    place $top.but54 \
        -in $top -x 0 -relx 0.67 -y 0 -rely 0.027 -width 137 -relwidth 0 \
        -height 26 -relheight 0 -anchor nw -bordermode ignore 
    place $top.but53 \
        -in $top -x 0 -relx 0.928 -y 0 -rely 0.027 -width 67 -relwidth 0 \
        -height 56 -relheight 0 -anchor nw -bordermode ignore 
    place $top.but62 \
        -in $top -x 0 -relx 0.928 -y 0 -rely 0.249 -width 67 -relwidth 0 \
        -height 26 -relheight 0 -anchor nw -bordermode ignore 
    place $top.but60 \
        -in $top -x 0 -relx 0.602 -y 0 -rely 0.027 -width 67 -relwidth 0 \
        -height 56 -relheight 0 -anchor nw -bordermode ignore 
    place $top.but57 \
        -in $top -x 0 -relx 0.67 -y 0 -rely 0.108 -width 137 -relwidth 0 \
        -height 26 -relheight 0 -anchor nw -bordermode ignore 
    place $top.tex66 \
        -in $top -x 0 -relx 0.602 -y 0 -rely 0.108 -width 0 -relwidth 0.061 \
        -height 0 -relheight 0.035 -anchor nw -bordermode ignore 
    place $top.but52 \
        -in $top -x 0 -relx 0.797 -y 0 -rely 0.108 -width 137 -relwidth 0 \
        -height 26 -relheight 0 -anchor nw -bordermode ignore 
    place $top.but67 \
        -in $top -x 0 -relx 0.797 -y 0 -rely 0.149 -width 137 -relwidth 0 \
        -height 26 -relheight 0 -anchor nw -bordermode ignore 
    place $top.but58 \
        -in $top -x 0 -relx 0.928 -y 0 -rely 0.108 -width 67 -relwidth 0 \
        -height 26 -relheight 0 -anchor nw -bordermode ignore 
    place $top.but68 \
        -in $top -x 0 -relx 0.928 -y 0 -rely 0.149 -width 67 -relwidth 0 \
        -height 26 -relheight 0 -anchor nw -bordermode ignore 
    place $top.can54 \
        -in $top -x 0 -relx 0.009 -y 0 -rely 0.289 -width 0 -relwidth 0.98 \
        -height 0 -relheight 0.599 -anchor nw -bordermode ignore 
    place $top.but47 \
        -in $top -x 0 -relx 0.014 -y 0 -rely 0.208 -width 70 -relwidth 0 \
        -height 26 -relheight 0 -anchor nw -bordermode ignore 
    place $top.but61 \
        -in $top -x 0 -relx 0.014 -y 0 -rely 0.249 -width 70 -relwidth 0 \
        -height 26 -relheight 0 -anchor nw -bordermode ignore 
    place $top.but48 \
        -in $top -x 0 -relx 0.014 -y 0 -rely 0.027 -width 70 -relwidth 0 \
        -height 60 -relheight 0 -anchor nw -bordermode ignore 
    place $top.fra59 \
        -in $top -x 0 -relx 0.43 -y 0 -rely 0.027 -width 0 -relwidth 0.168 \
        -height 0 -relheight 0.219 -anchor nw -bordermode ignore 
    place $top.but69 \
        -in $top -x 0 -relx 0.014 -y 0 -rely 0.168 -width 70 -relwidth 0 \
        -height 26 -relheight 0 -anchor nw -bordermode ignore 
    place $top.but49 \
        -in $top -x 0 -relx 0.014 -y 0 -rely 0.114 -width 70 -relwidth 0 \
        -height 26 -relheight 0 -anchor nw -bordermode ignore 
    place $top.tSc55 \
        -in $top -x 0 -relx 0.087 -y 0 -rely 0.892 -width 0 -relwidth 0.9 \
        -height 0 -relheight 0.026 -anchor nw -bordermode ignore 
    place $top.tSc56 \
        -in $top -x 0 -relx 0.009 -y 0 -rely 0.919 -width 0 -relwidth 0.9 \
        -height 0 -relheight 0.026 -anchor nw -bordermode ignore 
    place $top.ent71 \
        -in $top -x 0 -relx 0.91 -y 0 -rely 0.919 -width 84 -relwidth 0 \
        -height 19 -relheight 0 -anchor nw -bordermode ignore 
    place $top.ent70 \
        -in $top -x 0 -relx 0.009 -y 0 -rely 0.892 -width 84 -relwidth 0 \
        -height 19 -relheight 0 -anchor nw -bordermode ignore 
    place $top.tSc64 \
        -in $top -x 0 -relx 0.163 -y 0 -rely 0.254 -width 0 -relwidth 0.679 \
        -height 0 -relheight 0.027 -anchor nw -bordermode ignore 
    place $top.lis47 \
        -in $top -x 0 -relx 0.083 -y 0 -rely 0.027 -width 0 -relwidth 0.341 \
        -height 0 -relheight 0.219 -anchor nw -bordermode ignore 
    place $top.ent72 \
        -in $top -x 0 -relx 0.083 -y 0 -rely 0.254 -width 84 -relwidth 0 \
        -height 19 -relheight 0 -anchor nw -bordermode ignore 
    place $top.ent73 \
        -in $top -x 0 -relx 0.844 -y 0 -rely 0.254 -width 84 -relwidth 0 \
        -height 19 -relheight 0 -anchor nw -bordermode ignore 

    vTcl:FireEvent $base <<Ready>>
}

proc 36 {args} {return 1}


Window show .
set btop1 ""
if {$vTcl(borrow)} {
    set btop1 .bor[expr int([expr rand() * 100])]
    while {[lsearch $btop1 $vTcl(tops)] != -1} {
        set btop1 .bor[expr int([expr rand() * 100])]
    }
}
set vTcl(btop) $btop1
Window show .top1 $btop1
if {$vTcl(borrow)} {
    $btop1 configure -background plum
}

