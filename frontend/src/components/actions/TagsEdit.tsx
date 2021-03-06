import React from 'react'
import { IconButton, Dialog, DialogContent, DialogActions } from '@material-ui/core'
import TagsForm from '../forms/Tags'
import { withSnackbar, WithSnackbarProps } from 'notistack'
import LocalOfferOutlinedIcon from '@material-ui/icons/LocalOfferOutlined';


type Props = {
  id: number
  size: 'small' | 'medium'
}

type State = {
  dialogOpen: boolean
}

export class TagsEdit extends React.Component<Props, State> {
  state: State = {
    dialogOpen: false
  }

  close() {
    this.setState({ dialogOpen: false })
  }

  render() {
    return ([
      <IconButton
        size={this.props.size}
        title='Добавить тег'
        onClick={() => {
          this.setState({ dialogOpen: true })
        }}
        key={1}
      >
        <LocalOfferOutlinedIcon />
      </IconButton>,
      <Dialog
        open={this.state.dialogOpen}
        onClose={() => this.close()}
        key={2}
      >
        <DialogContent>
          <TagsForm id={this.props.id} onDone={() => this.close()} />
        </DialogContent>
        <DialogActions />
      </Dialog>
    ])
  }
}

export const FakeTagsEdit = withSnackbar((props: WithSnackbarProps & { size: 'small' | 'medium' }) => (
  <IconButton
    size={props.size}
    title='Добавить тег'
    onClick={() => props.enqueueSnackbar('Нужна авторизация')}
  >
    <LocalOfferOutlinedIcon />
  </IconButton>
))