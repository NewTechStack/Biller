import React, { Component } from 'react';
import PropTypes from 'prop-types';
import ChipsList from './ChipsList';
import './chips.scss';
import {Avatar, Checkbox as MuiCheckbox, MenuItem} from "@mui/material";
import Menu from "@mui/material/Menu";
import FormControlLabel from "@mui/material/FormControlLabel";

class Chips extends Component {
    constructor(props) {
        super(props);
        this.state = {
            chips: this.props.chips || [],
            KEY: {
                backspace: 8,
                tab: 9,
                enter: 13
            },
            disableInput: false,

            anchorElContactsMenu:null,
            newRoomCheck0:false
        };
        this.inputRef = React.createRef();
    }

    static getDerivedStateFromProps(nextProps, prevState) {
        if (prevState.chips.length === 0) {

            const disableInput =  nextProps.limit && nextProps.limit <= nextProps.chips.length;
            return { chips: nextProps.chips, disableInput, limitValidation: disableInput };
        }
        return null;
    }

    focusInput() {
        this.inputRef.current && this.inputRef.current.focus();
    }

    componentDidMount() {
        this.setChips(this.props.chips, true);
    }

    setChips(chips, save) {
        if (chips && chips.length) {
            const validChips = this.getValidChips(chips);
            console.log(validChips)
            const disableInput = this.props.limit && this.props.limit <= validChips.length;

            this.setState({ chips, limitValidation: disableInput, disableInput }, this.focusInput);

            if (save) {
                this.props.save(validChips);
            }
        }else{
            const validChips = this.getValidChips(chips);
            console.log(validChips)
            this.setState({chips})
            this.props.save(validChips);
        }
    }

    getValidChips(chips) {
        return chips.filter(chip => chip.valid);
    }

    onKeyDown(event) {
        const keyPressed = event.which;
        this.clearRequiredValidation();
        if (
            keyPressed === this.state.KEY.enter ||
            (keyPressed === this.state.KEY.tab && event.target.value)
        ) {
            event.preventDefault();
            this.updateChips(event);
        } else if (keyPressed === this.state.KEY.backspace) {
            const chips = this.state.chips;

            if (!event.target.value && chips.length) {
                this.deleteChip(chips[chips.length - 1]);
            }
        }
    }

    clearRequiredValidation() {
        this.setState({
            requiredValidation: false
        });
    }

    deleteChip(removedChip) {

        if (!removedChip) {
            return;
        }
        if (this.props.required && removedChip.valid && this.isOnlyOneValidChip()) {
            this.setState({
                requiredValidation: true
            });
            return;
        }else{
            const chips = this.state.chips.filter(chip => chip.key !== removedChip.key);

            this.setChips(chips, removedChip.valid);
            return true;
        }

    }

    isOnlyOneValidChip() {
        return this.getValidChips(this.state.chips).length <= 1;
    }

    updateChips(event) {

        const value = event.target.value;

        if (!value) {
            return;
        }

        const chipValue = value.trim().toLowerCase();

        // check if it is already exists
        const [chipExists] = this.state.chips.filter(chip => chip.email === chipValue);

        if (chipExists) {
            // @todo maybe get/set it on state
            event.target.value = '';
            return;
        }

        const valid = this.props.pattern ? this.props.pattern.test(chipValue) : true;
        const chips = this.state.chips.concat([{ email: chipValue, valid, key: Date.now() }]);

        this.setChips(chips, valid);

        event.target.value = '';
    }

    render() {
        let placeholder =
            !this.props.max || this.state.chips.length < this.props.max ? this.props.placeholder : '';
        return (
            <div>
                {/*<div className="row">
                    <div className="col-md-12" style={{ marginTop: 5 }}>
                        <FormControlLabel
                            control={
                                <MuiCheckbox
                                    checked={this.state.newRoomCheck0}
                                    onChange={(event, checked) => {
                                        if(this.state.newRoomCheck0 === false){
                                            (this.props.contacts || []).map((contact,key) => {
                                                event.persist()
                                                setTimeout(() => {
                                                    this.clearRequiredValidation();
                                                    event.target.value = contact.email
                                                    this.updateChips(event);
                                                },30)
                                            })
                                        }else{
                                            this.setState({chips:[]})
                                        }
                                        this.setState({
                                            newRoomCheck0: !this.state.newRoomCheck0
                                        })
                                    }}
                                    name="checkedNewRoom0"
                                />
                            }
                            label="Ajouter toute l'équipe d'OA Legal ?"
                        />
                    </div>
                </div>*/}

                <div className="chips" onClick={() => this.focusInput()}>
                    <ChipsList chips={this.state.chips} onChipClick={(event, chip) => {event.stopPropagation(); this.deleteChip(chip)}} />
                    { !this.state.disableInput &&
                    <input
                        type="text"
                        className="chips-input"
                        onFocus={() => this.clearRequiredValidation()}
                        placeholder={placeholder}
                        onKeyDown={e => this.onKeyDown(e)}
                        onBlur={(e) => {
                            this.updateChips(e)
                        }}
                        ref={this.inputRef}
                        onClick={(event) => this.props.openContactsMenuOnInputClick && this.props.openContactsMenuOnInputClick === true &&
                            this.setState({anchorElContactsMenu:event.currentTarget})}
                    />
                    }
                    <Menu id="contacts-menu"
                          anchorEl={this.state.anchorElContactsMenu}
                          keepMounted
                          open={Boolean(this.state.anchorElContactsMenu)}
                          onClose={() => {this.setState({anchorElContactsMenu:null})}}
                    >
                        {(this.props.contacts || []).map((contact, key) => (
                            <MenuItem
                                key={key}
                                value={contact.email}
                                onClick={(e) => {
                                    this.clearRequiredValidation();
                                    e.target.value = contact.email
                                    this.updateChips(e);
                                }}
                            >
                                <div style={{display:"flex"}}>
                                    <Avatar style={{marginLeft:10}}
                                            alt=""
                                            src={contact.imageUrl} />
                                    <div style={{marginTop:10,marginLeft:8}}>{contact.nom + ' ' + contact.prenom}</div>
                                </div>
                            </MenuItem>
                        ))}
                    </Menu>
                </div>
            </div>
        );
    }
}

Chips.propTypes = {
    chips: PropTypes.array,
    title: PropTypes.string,
    save: PropTypes.func,
    placeholder: PropTypes.string,
    pattern: PropTypes.instanceOf(RegExp),
    required: PropTypes.bool,
    requiredMessage: PropTypes.string,
    limit: PropTypes.oneOfType([
        PropTypes.string,
        PropTypes.number
    ]),
    limitMessage: PropTypes.string
};

export default Chips;