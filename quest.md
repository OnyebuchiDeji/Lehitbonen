### Date: Saturday 2nd August, 2025



##  Plan-Sat-2-Aug-2025 - Mon-4-Aug-2025

1.  Implement creation of program files, saving in the `programs` directory, and loading and displaying in the Main Screen as buttons
        -   Done
2.  Implement the initialization of the Editor Screen with the information of the selected program file displayed in the Main Screen as a Button, and such that when edited, once the Back button is pressed or the `Options->Save File` button is pressed, it saves the file and goes back to Main Screen. Also, implement the changing of the title label of the Editor Screen to be the file's name. Also, implement entering of the file's name using a button by the side that when pressed allows you to edit the name of the label via a Popup.  -   Done
3.  Implement syntax highlighting for glsl keywords.
4.  Add Button to switch to full screen, which changes the orientation for the Render Screen - Done
5.  Implement Trash Bin deleting 
6. Will also need to include popup for the Options buttons      ---     DONE
7.  Implement File Exporting to Android Directory- Done
8.  Implement Saving Snapshots Exporting to Android Directory- Done

##      Monday 5th August, 2025 ---     DONE
1.      Finish Render Screen's Functionality:
        -       Add another button to the Render Screen
                that allows maximizing the OpenGL Render's 
                resolution without flipping it to landscape.    ---     DONE
        +       SOL:
                I didn't add a new button, rather I used the same functionality and the modulus operator
                to change between modes.

2.      Finish Edit Screen Functionality:
        -       The Options Button at the top left corner.
>       Option Popups are a generic popup that is used for every option button that uses a Popup
                +       When clicked, it generates the Options Popup.
                +       This one has the options: 
                                "Save"
                                "Rename"
                                "Save As"
                        These options are Option Buttons. Their background normals are removed
                        and they're given almost-transparent backgrounds.
                        When these buttons are clicked, it generates an Action Popup
                        These Popups have the appropriate Title, a place for Input,
                                and a button to submit with the right button text       ---     DONE
        -       The Video Recording Button:
                Uses Pillow to record the sequence of pixel changes as the FBO is rendered to           ---     DONE

3.      Finish Main Screen's Functionality:
        -       Add the Menu Button icon at the Top Right    ---     DONE
                When clicked, it makes an Option Popup with the Options:
                        "Recycle Bin"
                        "About"                 ---     DONE
                When these Option Buttons are clicked, they go to the appropriate Screens. --- DONE
                +       The Recycle Bin Screen is like the Main Screen's Container. But it shows
                any Text Files that were deleted and moved into the Recycle Bin. It also has the title,
                "Recycle Bin"
                +       The About Screen has the title, "About", and it displays the About of the App. 
        -       Add the Delete Button, which has a Bin icon, beside each ProgramInfoButton so that when
                a button is clicked, it deletes (by moving to the recycle bin), the button besides it.
                However, when first clicked, it shows a Popup that prompts whether the user wants to delete it
                or not.                                                                         --- DONE
        -       Finally, add a lot of Program files and implement Scrolling on overflow --- DONE